from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Income, Expense, Category
from decimal import Decimal

class UserTests(APITestCase):

    def test_user_registration(self):
        url = reverse("register_user")
        data = {
            "username": "test_user",
            "password": "12345678",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "test_user")

    def test_user_login(self):
        User.objects.create_user(username="test_user", password="12345678")
        url = reverse("login_user")
        data = {
            "username": "test_user",
            "password": "12345678"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user", response.data)

class IncomeTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="12345678")
        self.category = Category.objects.create(name="Salary", user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_income(self):
        url = reverse("income-list-create")
        data = {
            "amount": "1000.00",
            "description": "Salary for August",
            "category": self.category.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Income.objects.count(), 1)
        self.assertEqual(Income.objects.get().description, "Salary for August")

    def test_list_incomes(self):
        Income.objects.create(
            user=self.user,
            amount="500.00",
            description="Bonus",
            category=self.category
        )
        url = reverse("income-list-create")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_income(self):
        income = Income.objects.create(
            user=self.user,
            amount="500.00",
            description="Bonus",
            category=self.category
        )
        url = reverse("income-detail", args=[income.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], "Bonus")

    def test_update_income(self):
        income = Income.objects.create(
            user=self.user,
            amount="500.00",
            description="Bonus",
            category=self.category
        )
        url = reverse("income-detail", args=[income.id])
        data = {
            "amount": "600.00",
            "description": "Updated Bonus",
            "category": self.category.id
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        income.refresh_from_db()
        self.assertEqual(income.amount, Decimal("600.00"))
        self.assertEqual(income.description, "Updated Bonus")

    def test_delete_income(self):
        income = Income.objects.create(
            user=self.user,
            amount="500.00",
            description="Bonus",
            category=self.category
        )
        url = reverse("income-detail", args=[income.id])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Income.objects.count(), 0)

class ExpenseTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="12345678")
        self.category = Category.objects.create(name="Rent", user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_expense(self):
        url = reverse("expense-list-create")
        data = {
            "amount": "300.00",
            "description": "Monthly Rent",
            "category": self.category.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(Expense.objects.get().description, "Monthly Rent")

    def test_list_expenses(self):
        Expense.objects.create(
            user=self.user,
            amount="150.00",
            description="Utilities",
            category=self.category
        )
        url = reverse("expense-list-create")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_expense(self):
        expense = Expense.objects.create(
            user=self.user,
            amount="150.00",
            description="Utilities",
            category=self.category
        )
        url = reverse("expense-detail", args=[expense.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], "Utilities")

    def test_update_expense(self):
        expense = Expense.objects.create(
            user=self.user,
            amount="150.00",
            description="Utilities",
            category=self.category
        )
        url = reverse("expense-detail", args=[expense.id])
        data = {
            "amount": "200.00",
            "description": "Updated Utilities",
            "category": self.category.id
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expense.refresh_from_db()
        self.assertEqual(expense.amount, Decimal("200.00"))
        self.assertEqual(expense.description, "Updated Utilities")

    def test_delete_expense(self):
        expense = Expense.objects.create(
            user=self.user,
            amount="150.00",
            description="Utilities",
            category=self.category
        )
        url = reverse("expense-detail", args=[expense.id])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Expense.objects.count(), 0)


class CategoryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="12345678")
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(user=self.user, name="Food")

    def test_create_category(self):
        url = reverse("category-list-create")
        data = {
            "name": "Entertainment"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)  # Include the initial category
        self.assertEqual(Category.objects.latest('id').name, "Entertainment")

    def test_list_categories(self):
        url = reverse("category-list-create")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only the initial category created in setUp

    def test_retrieve_category(self):
        url = reverse("category-detail", args=[self.category.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Food")

    def test_update_category(self):
        url = reverse("category-detail", args=[self.category.id])
        data = {
            "name": "Updated Food"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Updated Food")

    def test_delete_category(self):
        url = reverse("category-detail", args=[self.category.id])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)