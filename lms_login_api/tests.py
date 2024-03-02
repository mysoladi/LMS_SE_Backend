from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from utils.models import CustomUser

class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        url = reverse('user-list')
        data = {
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
            'sec_answer': 'answer123',
            'username': 'johndoe'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().email, 'test@example.com')

class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="johndoe",  # Here's the corrected username assignment
            email='test@example.com',
            password='Password@123',
            first_name='John',
            last_name='Doe',
            sec_answer='answer123',
        )

    def test_user_login(self):
        url = "http://127.0.0.1:8000/login/"
        data = {'username': 'johndoe', 'password': 'Password@123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)