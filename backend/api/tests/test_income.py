from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import User, Income, Category
from decimal import Decimal

class IncomeTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="12345678")
        self.category = Category.objects.create(name="Salary", user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_income(self):
        url = reverse("income")
        data = {
            "amount": "1000.00",
            "description": "Salary for August",
            "category": self.category.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Income.objects.count(), 1)
        self.assertEqual(Income.objects.get().description, "Salary for August")
        self.assertEqual(Income.objects.get().__str__() , "1000.00 by test_user")
        

    def test_list_incomes(self):
        Income.objects.create(
            user=self.user,
            amount="500.00",
            description="Bonus",
            category=self.category
        )
        url = reverse("income")
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
        url = reverse("income", args=[income.id])
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
        url = reverse("income", args=[income.id])
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
        url = reverse("income", args=[income.id])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Income.objects.count(), 0)