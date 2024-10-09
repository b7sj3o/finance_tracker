from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import User, Expense, Category
from decimal import Decimal


class ExpenseTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test_user", chat_id=111, password="12345678")
        self.category = Category.objects.create(name="Rent", user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_expense(self):
        # ERROR - NOT ENOUGH BALANCE
        url = reverse("expense")
        data = {
            "amount": "300.00",
            "description": "Monthly Rent",
            "category": self.category.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # ADD SOME BALANCE
        self.user.balance = 500
        
        # SUCCESS
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(Expense.objects.get().description, "Monthly Rent")
        self.assertEqual(Expense.objects.get().__str__() , "300.00 by test_user")
        

    def test_list_expenses(self):
        Expense.objects.create(
            user=self.user,
            amount="150.00",
            description="Utilities",
            category=self.category
        )
        url = reverse("expense")
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
        url = reverse("expense", args=[expense.id])
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
        url = reverse("expense", args=[expense.id])
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
        url = reverse("expense", args=[expense.id])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Expense.objects.count(), 0)
