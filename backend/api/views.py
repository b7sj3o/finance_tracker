"""
Views for handling API requests in the finance tracker application.
"""

from django.contrib.auth import login as auth_login
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken

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
    AuthMixin,
    ListMixin,
    CreateMixin,
    RetrieveMixin,
    UpdateMixin,
    DeleteMixin,
)


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
            response = Response(response_data, status=status.HTTP_200_OK)
            response.set_cookie(
                key="sessionid",
                value=request.session.session_key,
                httponly=True,
                samesite="Lax",
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCreateExpenseView(
    ContentTypeValidationMixin, UserFilteredMixin, generics.ListCreateAPIView
):
    """
    List and create expenses with content type validation.
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class RetrieveUpdateDestroyExpenseView(
    ContentTypeValidationMixin, UserFilteredMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    Retrieve, update, or destroy an expense with content type validation.
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer



class ListCreateIncomeView(
    ContentTypeValidationMixin, UserFilteredMixin, generics.ListCreateAPIView
):
    """
    List and create incomes with content type validation.
    """
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


class RetrieveUpdateDestroyIncomeView(
    ContentTypeValidationMixin, UserFilteredMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    Retrieve, update, or destroy an income with content type validation.
    """
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer



class ListCreateCategoryView(
    ContentTypeValidationMixin, UserFilteredMixin, generics.ListCreateAPIView
):
    """
    List and create categories with content type validation.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class RetrieveUpdateDestroyCategoryView(
    ContentTypeValidationMixin, UserFilteredMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    Retrieve, update, or destroy a category with content type validation.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
#TODO доробити всюди логи