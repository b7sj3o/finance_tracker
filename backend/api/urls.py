from django.urls import path
from .views import (
    UserCreateView,
    LoginView,
    IncomeView,
    ExpenseView,
    CategoryView,
    GetUserView,
    GenerateCSVReportView,
    WeeklyExpensesView,
    MonthlyExpensesView,
    WeeklyIncomesView,
    MonthlyIncomesView,
    GenerateExcelReportView,
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
    path("get_user/", GetUserView.as_view(), name="get_user"),
    path(
        "generate_csv_report/",
        GenerateCSVReportView.as_view(),
        name="generate_csv_report",
    ),
    path(
        "generate_excel_report/",
        GenerateExcelReportView.as_view(),
        name="generate_excel_report",
    ),
    path("weekly_expenses/", WeeklyExpensesView.as_view(), name="weekly_expenses"),
    path("monthly_expenses/", MonthlyExpensesView.as_view(), name="monthly_expenses"),
    path("weekly_incomes/", WeeklyIncomesView.as_view(), name="weekly_incomes"),
    path("monthly_incomes/", MonthlyIncomesView.as_view(), name="montly_incomes"),
]
