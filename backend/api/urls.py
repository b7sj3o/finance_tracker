from django.urls import path
from .views import (
    UserCreateView,
    LoginView,
    ListCreateIncomeView,
    RetrieveUpdateDestroyIncomeView,
    ListCreateExpenseView,
    RetrieveUpdateDestroyExpenseView,
    ListCreateCategoryView,
    RetrieveUpdateDestroyCategoryView,
)

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register_user"),
    path("login/", LoginView.as_view(), name="login_user"),
    path("income/", ListCreateIncomeView.as_view(), name="income-list-create"),
    path(
        "income/<int:pk>/",
        RetrieveUpdateDestroyIncomeView.as_view(),
        name="income-detail",
    ),
    path("expense/", ListCreateExpenseView.as_view(), name="expense-list-create"),
    path(
        "expense/<int:pk>/",
        RetrieveUpdateDestroyExpenseView.as_view(),
        name="expense-detail",
    ),
    path("category/", ListCreateCategoryView.as_view(), name="category-list-create"),
    path(
        "category/<int:pk>/",
        RetrieveUpdateDestroyCategoryView.as_view(),
        name="category-detail",
    ),
]
