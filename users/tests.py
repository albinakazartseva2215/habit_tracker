from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserModelTestCase(APITestCase):
    """Тесты для UserCreateAPIView"""

    def setUp(self):
        self.create_url = reverse("users:register")
        self.valid_data = {
            "email": "test@example.com",
            "password": "securepassword123",
            "city": "Москва",
            "tg_chat_id": "123456",
        }

    def test_successful_user_creation(self):
        """Проверка успешного создания пользователя"""
        response = self.client.post(self.create_url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.get()
        self.assertEqual(user.email, self.valid_data["email"])
        self.assertTrue(user.is_active)

    def test_duplicate_email_rejection(self):
        """Проверка уникальности email"""
        self.client.post(self.create_url, self.valid_data)
        response = self.client.post(self.create_url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(User.objects.count(), 1)
