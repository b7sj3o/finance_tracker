from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from api.models import Income, Expense, User, Category
from api.admin import TransferingAdmin
from datetime import datetime


class AdminTest(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.income_admin = TransferingAdmin(Income, self.site)
        self.expense_admin = TransferingAdmin(Expense, self.site)
        
        self.user = User.objects.create_user(username="test_user", password="12345678")
        self.category = Category.objects.create(user=self.user, name="Food")

        self.income = Income.objects.create(
            user=self.user,
            description="Test income description that is longer than 15 characters",
            amount=100,
            category=self.category
        )

        self.expense = Expense.objects.create(
            user=self.user,
            description="Short desc",
            amount=50,
            category=self.category
        )

    def test_description_short(self):
        short_desc_income = self.income_admin.description_short(self.income)
        self.assertEqual(short_desc_income, "Test income des")

        short_desc_expense = self.expense_admin.description_short(self.expense)
        self.assertEqual(short_desc_expense, "Short desc")

    def test_created_formatted(self):
        created_formatted_income = self.income_admin.created_formatted(self.income)
        self.assertEqual(created_formatted_income, datetime.now().strftime("%d:%m:%Y, %H:%M"))

        created_formatted_expense = self.expense_admin.created_formatted(self.expense)
        self.assertEqual(created_formatted_expense, datetime.now().strftime("%d:%m:%Y, %H:%M"))

    def test_updated_formatted(self):
        updated_formatted_income = self.income_admin.updated_formatted(self.income)
        self.assertEqual(updated_formatted_income, datetime.now().strftime("%d:%m:%Y, %H:%M"))

        updated_formatted_expense = self.expense_admin.updated_formatted(self.expense)
        self.assertEqual(updated_formatted_expense, datetime.now().strftime("%d:%m:%Y, %H:%M"))
