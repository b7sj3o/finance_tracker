from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import login as auth_login
from .models import User, Expense, Income, Category
from .serializers import (
    UserSerializer,
    LoginSerializer,
    ExpenseSerializer,
    IncomeSerializer,
    CategorySerializer,
)
import logging

logger = logging.getLogger(__name__)


class UserFilteredMixin(generics.GenericAPIView):
    """
    Mixin to filter queryset by current user.
    """

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        if request.content_type != "application/json":
            return Response(
                {"detail": "Content-Type must be application/json"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "User created successfully",
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        if request.content_type != "application/json":
            return Response(
                {"detail": "Content-Type must be application/json"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            auth_login(request, user)

            response_data = {
                "user": {
                    "username": user.username,
                }
            }

            response = Response(response_data, status=status.HTTP_200_OK)
            response.set_cookie(
                key="sessionid",
                value=request.session.session_key,
                httponly=True,
                samesite="Lax",
            )
            return response

        logger.error(f"Login error: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCreateExpenseView(UserFilteredMixin, generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def post(self, request, *args, **kwargs):
        if request.content_type != "application/json":
            return Response(
                {"detail": "Content-Type must be application/json"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        return super().post(request, *args, **kwargs)


class RetrieveUpdateDestroyExpenseView(
    UserFilteredMixin, generics.RetrieveUpdateDestroyAPIView
):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def put(self, request, *args, **kwargs):
        if request.content_type != "application/json":
            return Response(
                {"detail": "Content-Type must be application/json"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if request.content_type != "application/json":
            return Response(
                {"detail": "Content-Type must be application/json"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        return super().patch(request, *args, **kwargs)

    def deletes(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ListCreateIncomeView(UserFilteredMixin, generics.ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def post(self, request, *args, **kwargs):
        if request.content_type != "application/json":
            return Response(
                {"detail": "Content-Type must be application/json"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        return super().post(request, *args, **kwargs)


class RetrieveUpdateDestroyIncomeView(
    UserFilteredMixin, generics.RetrieveUpdateDestroyAPIView
):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def put(self, request, *args, **kwargs):
        if request.content_type != "application/json":
            return Response(
                {"detail": "Content-Type must be application/json"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if request.content_type != "application/json":
            return Response(
                {"detail": "Content-Type must be application/json"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        return super().patch(request, *args, **kwargs)

    def deletes(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ListCreateCategoryView(UserFilteredMixin, generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def post(self, request, *args, **kwargs):
        if request.content_type != "application/json":
            return Response(
                {"detail": "Content-Type must be application/json"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        return super().post(request, *args, **kwargs)


class RetrieveUpdateDestroyCategoryView(
    UserFilteredMixin, generics.RetrieveUpdateDestroyAPIView
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def put(self, request, *args, **kwargs):
        if request.content_type != "application/json":
            return Response(
                {"detail": "Content-Type must be application/json"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if request.content_type != "application/json":
            return Response(
                {"detail": "Content-Type must be application/json"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        return super().patch(request, *args, **kwargs)

    def deletes(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
