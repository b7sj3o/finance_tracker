from django.urls import path
from .views import (
    UserCreateView,
    LoginView,
    IncomeView,
    ExpenseView,
    CategoryView,
)

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register_user"),
    path("login/", LoginView.as_view(), name="login_user"),
    path("income/", IncomeView.as_view(), name="income"),
    path("income/<int:pk>/", IncomeView.as_view(), name="income"),
    path("expense/<int:pk>", ExpenseView.as_view(), name="expense"),
    path("expense/", ExpenseView.as_view(), name="expense"),
    path("category/", CategoryView.as_view(), name="category"),
    path("category/<int:pk>", CategoryView.as_view(), name="category"),
]
