"""
Views for handling API requests in the finance tracker application.
"""

from django.contrib.auth import login as auth_login
from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

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
    # AuthMixin,
    #ListMixin,
    CreateMixin,
    #RetrieveMixin,
    #UpdateMixin,
    #DeleteMixin,
)


class BaseCRUDView(
    ContentTypeValidationMixin,
    UserFilteredMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    Base CRUD View for executing simple operations described in CRUD

    required fields:
    queryset = *Model*.objects.all()
    serializer_class = *ModelSerializer*
    """

    def get(self, request, *args, **kwargs):
        return self.operation(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.operation(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.operation(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.operation(request, *args, **kwargs)

    def operation(self, request, *args, **kwargs):
        methods = {
            "GET": "retrieve",
            "POST": "create",
            "PUT": "update",
            "PATCH": "partial_update",
            "DELETE": "destroy",
        }
        method = methods[request.method]
        if "pk" in kwargs:
            response = getattr(self, method)(request, *args, **kwargs)
            if response.status_code == "400":
                return Response(response.data, status=status.HTTP_400_BAD_REQUEST)
            return response
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
            response = Response(response_data, status=status.HTTP_200_OK)
            response.set_cookie(
                key="sessionid",
                value=request.session.session_key,
                httponly=True,
                samesite="Lax",
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseView(BaseCRUDView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class IncomeView(BaseCRUDView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


class CategoryView(BaseCRUDView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
