from rest_framework import status
from rest_framework.test import APIClient, APITestCase

class Base(APITestCase):
    def setUp(self):
        # Set up the client
        self.client = APIClient()

        self.user_data = {
                            'username': 'username',
                            'email': 'email@example.com',
                            'password': 'password'
                        }
        # url
        self.url = "/api/"

class UserRegistrationTests(Base):
    def setUp(self):
        super().setUp()

    def test_user_registration(self):
        url = f"{self.url}register/"
        
        # test
        response = self.client.post(url, self.user_data, format='json')

        # validate
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class  UserLoginTests(Base):
    def setUp(self) -> None:
        super().setUp()

        # Register user 
        url = f"{self.url}register/"
        response = self.client.post(url, self.user_data, format='json')

        # URL
        self.url = f"{self.url}login/"
    
    def test_user_login_exists(self):
        # test
        response = self.client.post(self.url, self.user_data, format='json')

        # validate
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


    def test_user_login_not_exists(self):
        not_user = {
            'username': 'username2',
            'email': 'email@example.com',
            'password': 'password'
        }
        # test
        response = self.client.post(self.url, not_user, format='json')
        
        # validate
        self.assertEqual(response.status_code, 401) 
        self.assertIn(response.data['error'], 'Invalid Credentials') 




