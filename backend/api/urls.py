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
    BotUserCreateView,
    BotLoginView,
    BotListCreateIncomeView,
    BotRetrieveUpdateDestroyIncomeView,
    BotListCreateExpenseView,
    BotRetrieveUpdateDestroyExpenseView,
    BotListCreateCategoryView,
    BotRetrieveUpdateDestroyCategoryView,
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
    path("bot/register/", BotUserCreateView.as_view(), name="bot_register_user"),
    path("bot/login/", BotLoginView.as_view(), name="bot_login_user"),
    path(
        "bot/income/", BotListCreateIncomeView.as_view(), name="bot_income-list-create"
    ),
    path(
        "bot/income/<int:pk>/",
        BotRetrieveUpdateDestroyIncomeView.as_view(),
        name="bot_income-detail",
    ),
    path(
        "bot/expense/",
        BotListCreateExpenseView.as_view(),
        name="bot_expense-list-create",
    ),
    path(
        "bot/expense/<int:pk>/",
        BotRetrieveUpdateDestroyExpenseView.as_view(),
        name="bot_expense-detail",
    ),
    path(
        "bot/category/",
        BotListCreateCategoryView.as_view(),
        name="bot_category-list-create",
    ),
    path(
        "bot/category/<int:pk>/",
        BotRetrieveUpdateDestroyCategoryView.as_view(),
        name="bot_category-detail",
    ),
]
