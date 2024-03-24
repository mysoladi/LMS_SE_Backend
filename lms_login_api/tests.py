from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import CustomUser
import uuid


class UserTests(TestCase):
    user_data = {}
    client = None
    user = None

    def set_up(self):
        self.client = APIClient()
        unique_suffix = uuid.uuid4()  # Generates a unique UUID
        self.user_data = {
            'email': f'test{unique_suffix}@gmail.com',
            'username': f'{unique_suffix}testing',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'sec_answer': 'test_answer',
            'user_role': 'Student'
        }
        # self.user = CustomUser.objects.create_user(**self.user_data)

    def test_1_create_user(self):
        self.set_up()
        url = reverse('create_user') 
        response = self.client.post(url, self.user_data, format='json')
        # print(self.user_data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('email' in response.data)

    def test_2_user_login(self):
        self.set_up()
        self.user = CustomUser.objects.create_user(**self.user_data)
        print(self.user)
        url = reverse('user_login')
        login_credentials = {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        }
        response = self.client.post(url,login_credentials)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

    def test_3_change_password(self):
        self.set_up()
        self.user = CustomUser.objects.create_user(**self.user_data)
        url = reverse('sec_change_password')  # Use the actual name used in your urls.py
        new_password = 'newTestPassword123'
        response = self.client.put(url, {'email': self.user_data['email'], 'password': new_password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))
