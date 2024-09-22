"""
Views for handling API requests in the finance tracker application.
"""

from django.contrib.auth import login as auth_login
from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from typing import Union
from django.db.models import Sum, QuerySet
import csv
from datetime import datetime, timedelta

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
            expenses = request.user.expense_set.all().order_by("created")
            incomes = request.user.income_set.all().order_by("created")
            
            transfers = sorted(
                list(expenses) + list(incomes),
                key=lambda transfer: transfer.created
            )
            
            csv_rows = (
                [
                    transfer.created.strftime("%d.%m.%Y, %H:%M:%S"),
                    transfer.__class__.__name__,
                    transfer.amount,
                    transfer.description or "-",
                    transfer.category or "-"
                ] for transfer in transfers
            ) 
            
            
            with open(f"{request.user.username}-report.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Data", "Type", "Amount", "Description", "Category"])
                writer.writerows(csv_rows)
            

            return Response(data={"message": "report.csv"}, status=status.HTTP_201_CREATED)
                
        except User.DoesNotExist:
            return Response(data={"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(data={"message": f"{ex}"}, status=status.HTTP_400_BAD_REQUEST)
        

class GenerateTimeView:
    
    @staticmethod
    def generate_time(request, transfer_type: Union[Income, Expense], days: int, *args, **kwargs):
        transfers = transfer_type.objects.filter(user=request.user).order_by("created")

        if not transfers:
            return Response({"message": f"No {transfer_type.__name__.lower()}s found."}, status=status.HTTP_404_NOT_FOUND)
        
        start_of_week = transfers[0].created.date()
        end_of_week = start_of_week + timedelta(days=(days-1))

        time_transfers = []

        while start_of_week <= datetime.now().date():
            time_period = "{}-{}".format(
                start_of_week.strftime("%d.%m.%Y"),
                end_of_week.strftime("%d.%m.%Y")
            )
            
            filtered_transfers = transfers.filter(created__gte=start_of_week, created__lte=end_of_week)
            
            if filtered_transfers:
                total_amount = filtered_transfers.aggregate(total=Sum("amount"))["total"] or 0
                time_transfers.append({
                    "period": time_period,
                    "total_amount": total_amount,
                    "days": GenerateTimeView.count_transfers_by_day(transfers, days, start_of_week)
                })
                
            start_of_week = end_of_week + timedelta(days=1)
            end_of_week = start_of_week + timedelta(days=(days-1))
            
        return Response(time_transfers, status=status.HTTP_200_OK)
    
    @staticmethod 
    def count_transfers_by_day(transfers: QuerySet, days: int,  current_date):
        daily_transfers = []
        for _ in range(days):
            filtered_transfers = transfers.filter(created__date=current_date)

            if filtered_transfers:
                total_amount = filtered_transfers.aggregate(total=Sum("amount"))["total"] or 0
                daily_transfers.append({
                    "date": current_date.strftime("%d.%m.%Y"),
                    "total_amount": total_amount,
                })

            current_date += timedelta(days=1)
        
        return daily_transfers

class WeeklyExpensesView(generics.RetrieveAPIView):
    queryset = Expense.objects.all()
    
    def get(self, request, *args, **kwargs):
        return GenerateTimeView.generate_time(request, Expense, 7, args, kwargs)
    
    
class MonthlyExpensesView(generics.RetrieveAPIView):
    
    def get(self, request, *args, **kwargs):
        return GenerateTimeView.generate_time(request, Expense, 30, args, kwargs)
            

class WeeklyIncomesView(generics.RetrieveAPIView):
    
    def get(self, request, *args, **kwargs):
        return GenerateTimeView.generate_time(request, Income, 7, args, kwargs)
    
    
class MonthlyIncomesView(generics.RetrieveAPIView):
    
    def get(self, request, *args, **kwargs):
        return GenerateTimeView.generate_time(request, Income, 30, args, kwargs)
    

