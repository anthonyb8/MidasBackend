from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status

USER = {
        'username': 'username',
        'email': 'email@example.com',
        'password': 'password'
        }

class UserRegistrationTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        data = {
            'username': 'username',
            'email': 'email@example.com',
            'password': 'password'
        }
        response = self.client.post('/account/register/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class  UserLoginTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
    
    def test_user_login(self):
        response = self.client.post('/api/account/register/', USER, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {response.data["token"]}')

    def test_user_login(self):
        # You might need to create a user first if it's not already created
        data = {'username': 'anthony', 'password': 'testing123'}
        response = self.client.post('/api/account/login/', data, format='json')
        self.assertEqual(response.status_code, 200)  # Assuming 200 is the status for successful login
        self.assertIn('token', response.data)  # Check if token is in response

class  UserLoginTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
    
    def test_user_logout(self):
        # First login or create a user and login to obtain a token
        self.test_user_login()  # Or however you obtain a token

        # Assuming the token is stored in self.token after login
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post('https://midasbackend-157a5aab9f51.herokuapp.com/account/logout/', format='json')
        self.assertEqual(response.status_code, 204)  # Assuming 204 is the status for successful logout
        # Clear the credentials after logout
        self.client.credentials()



