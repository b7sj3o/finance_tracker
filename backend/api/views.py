from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login as auth_login
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Expense, Income, Category
from .serializers import (
    UserSerializer, 
    LoginSerializer, 
    ExpenseSerializer, 
    IncomeSerializer,
    CategorySerializer
)
import logging

logger = logging.getLogger(__name__)


class UserFilteredMixin(generics.GenericAPIView):
    """
    Get current user objects 
    """
    def get_queryset(self):
        """
        Filter queryset based on the current user.
        """
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Save the object with the current user as the user field.
        """
        serializer.save(user=self.request.user)
    

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "User created successfully",
                    "user": UserSerializer(username).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            auth_login(request, user)

            response_data = {
                "user": {
                    "username": user.username,
                }
            }

            response = Response(response_data, status=status.HTTP_200_OK)
            response.set_cookie(key='sessionid', value=request.session.session_key, httponly=True, samesite='Lax')
            return response
        
        logger.error(f'Login error: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCreateExpenseView(UserFilteredMixin, generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class RetrieveUpdateDestroyExpenseView(UserFilteredMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class ListCreateIncomeView(UserFilteredMixin, generics.ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


class RetrieveUpdateDestroyIncomeView(UserFilteredMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


class ListCreateCategoryView(UserFilteredMixin, generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RetrieveUpdateDestroyCategoryView(UserFilteredMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer