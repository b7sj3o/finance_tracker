from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import User

class UserTests(APITestCase):

    def test_user_registration(self):
        url = reverse("register_user")
        data = {
            "username": "test_user",
            "chat_id": "111",
            "password": "12345678",
        }
        response = self.client.post(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "test_user")
