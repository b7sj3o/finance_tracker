from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import User

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
        # TEST SUCCESS USER
        User.objects.create_user(username="test_user", password="12345678")
        url = reverse("login_user")
        data = {
            "username": "test_user",
            "password": "12345678"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user", response.data)
        
        # TEST INVALID PASSWORD
        data = {
            "username": "test_user",
            "password": "123"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # TEST NO USERNAME
        data = {
            "username": "",
            "password": "12345678"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
