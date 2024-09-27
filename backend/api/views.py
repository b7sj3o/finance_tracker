"""
Views for handling API requests in the finance tracker application.
"""

from django.contrib.auth import login as auth_login
from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from typing import Union
from django.db.models import Sum, QuerySet
import openpyxl
import csv
from datetime import datetime, timedelta

from .utils import (
    create_report_data,
    generate_transfers
)
from .models import User, Expense, Income, Category
from .serializers import (
    UserSerializer,
    LoginSerializer,
    ExpenseSerializer,
    IncomeSerializer,
    CategorySerializer,
)
from .mixins import (
    UserFilteredMixin,
    ContentTypeValidationMixin,
    CreateMixin,
)


class BaseCRUDView(
    ContentTypeValidationMixin,
    UserFilteredMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView    
):
    """
    Base CRUD View for executing simple operations described in CRUD
    
    required fields:
    queryset = *Model*.objects.all()
    serializer_class = *ModelSerializer*
    """
    
        
    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    
    def post(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.create(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


    def put(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.update(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


    def patch(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.partial_update(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    
    def delete(self, request, *args, **kwargs):
        if "pk" in kwargs:
            self.destroy(request, *args, **kwargs)
            return Response({"message": "Item was deleted"}, status=status.HTTP_200_OK)
        return self.list(request, *args, **kwargs)
        

class UserCreateView(ContentTypeValidationMixin, generics.CreateAPIView):
    """
    Create a new user with content type validation.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class LoginView(ContentTypeValidationMixin, CreateMixin, generics.GenericAPIView):
    """
    Log in a user and set a session cookie.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            auth_login(request, user)
            response_data = {
                "status": "success",
                "message": "User logged in successfully.",
                "user": {"username": user.username},
            }
            response = Response(data=response_data, status=status.HTTP_200_OK)
            response.set_cookie(
                key="sessionid",
                value=request.session.session_key,
                httponly=True,
                samesite="Lax",
            )
            return response
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseView(BaseCRUDView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    
    
    def post(self, request, *args, **kwargs):
        amount = float(request.data.get("amount"))
        if request.user.balance - amount < 0:
            return Response(data={"message":"You don't have enough balance to perform this operation"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        response = self.create(request, *args, **kwargs)
        request.user.update_balance()
        return response
        
    
class IncomeView(BaseCRUDView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    
    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        request.user.update_balance()
        return response


class CategoryView(BaseCRUDView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    

class GetUserView(generics.RetrieveAPIView):
    # def get(self, request, *args, **kwargs):
    #     serializer = UserSerializer(request.user)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class GenerateCSVReportView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        try:
            csv_titles, csv_rows = create_report_data(request)
            
            
            with open(f"../reports/{request.user.chat_id}-report.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(csv_titles)
                writer.writerows(csv_rows)
            

            return Response(data={"message": f"{request.user.chat_id}-report.csv"}, status=status.HTTP_201_CREATED)
                
        except User.DoesNotExist:
            return Response(data={"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return Response(data={"message": f"{ex}"}, status=status.HTTP_400_BAD_REQUEST)
        

class GenerateExcelReportView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        
        try:
            excel_titles, excel_rows = create_report_data(request)

            
            # with open(f"../reports/{user.chat_id}-report.excel", "w+", newline="") as file:
            excel_file = openpyxl.Workbook()
            excel_file_list = excel_file.active
            
            excel_file_list.column_dimensions['A'].width = 20  # Дата
            excel_file_list.column_dimensions['B'].width = 10  # Тип (Expense | Income)
            excel_file_list.column_dimensions['C'].width = 7  # Сума
            excel_file_list.column_dimensions['D'].width = 30  # Опис
            excel_file_list.column_dimensions['E'].width = 20  # Категорія
            
            excel_file_list.append(excel_titles)
            
            for row in excel_rows:
                excel_file_list.append(row)            
            
            excel_file.save(f"../reports/{request.user.chat_id}-report.xlsx")
            
            return Response(data={"message": f"{request.user.chat_id}-report.excel"}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response(data={"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return Response(data={"message": f"{ex}"}, status=status.HTTP_400_BAD_REQUEST)
            
    
class WeeklyExpensesView(generics.RetrieveAPIView):
    queryset = Expense.objects.all()
    
    def get(self, request, *args, **kwargs):
        return generate_transfers(request, Expense, 7, args, kwargs)
    
    
class MonthlyExpensesView(generics.RetrieveAPIView):
    
    def get(self, request, *args, **kwargs):
        return generate_transfers(request, Expense, 30, args, kwargs)
            

class WeeklyIncomesView(generics.RetrieveAPIView):
    
    def get(self, request, *args, **kwargs):
        return generate_transfers(request, Income, 7, args, kwargs)
    
    
class MonthlyIncomesView(generics.RetrieveAPIView):
    
    def get(self, request, *args, **kwargs):
        return generate_transfers(request, Income, 30, args, kwargs)
    

