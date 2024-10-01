from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import User, Category


class CategoryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", chat_id=111, password="12345678")
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(user=self.user, name="Food")
        
    def test_create_category(self):
        url = reverse("category")
        data = {
            "name": "entertainment"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)  # Include the initial category
        self.assertEqual(Category.objects.latest('id').name, "entertainment")
        self.assertEqual(Category.objects.latest('id').__str__() , "Entertainment")

    def test_list_categories(self):
        url = reverse("category")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only the initial category created in setUp

    def test_retrieve_category(self):
        url = reverse("category", args=[self.category.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Food")

    def test_update_category(self):
        url = reverse("category", args=[self.category.id])
        data = {
            "name": "Updated Food"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Updated Food")

    def test_delete_category(self):
        url = reverse("category", args=[self.category.id])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)
