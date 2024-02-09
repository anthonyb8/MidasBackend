from django.test import TestCase
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
# from .models import Symbol, Equity, Commodity, Future, Cryptocurrency, Option
from rest_framework.test import APIClient
from django.test import TestCase
from .models import Symbol, Equity
from rest_framework.authtoken.models import Token
from account.views import CustomUser

class SymbolAPITests(TestCase):
    USER = {
            'username': 'username',
            'email': 'email@example.com',
            'password': 'password'
    }

    def setUp(self):
        self.client = APIClient()
        response = self.client.post('/api/account/register/', self.USER, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {response.data["token"]}')

        self.data = {
            "symbol_data": {
                "symbol": "AAPL",
                "security_type": "EQUITY"
            },
            "company_name": "Apple Inc.",
            "exchange": "NYSE",
            "currency": "USD",
            "industry": "Technology",
            "description": "Description of Example Company",
            "market_cap": 5000000,
            "shares_outstanding": 1000000
        }

        self.create_valid_equity()

    def create_valid_equity(self):
        response = self.client.post('/api/equities/', self.data, format='json')
        self.assertEqual(response.status_code, 201)


    def test_get_all_symbols(self):
        response = self.client.get('/api/symbols/', format='json')
        self.assertEqual(response.status_code, 200)
        # Additional assertions can be made based on the expected response structure

    def test_get_symbol_by_id(self):
        # Assuming an symbol with ID 1 exists
        response = self.client.get('/api/symbols/1/', format='json')
        self.assertEqual(response.status_code, 200)
        # Additional assertions based on the expected symbol details

    def test_get_symbol_by_symbol(self):
        # Assuming an symbol with symbol 'AAPL' exists
        response = self.client.get('/api/symbols/?symbol=AAPL', format='json')
        self.assertEqual(response.status_code, 200)
        # Additional assertions based on the expected symbol details

    def test_delete_symbol(self):
        # Create an symbol to be deleted or assume one exists
        # For example, if an symbol with ID 4 exists
        response = self.client.delete('/api/symbols/4/', format='json')
        self.assertEqual(response.status_code, 204)  # No Content on successful deletion
        # You might also want to check if the symbol is indeed deleted
        check_response = self.client.get('/api/symbols/4/', format='json')
        self.assertEqual(check_response.status_code, 404)

# class EquityAPITests(TestCase):
        
#     USER = {
#             'username': 'username',
#             'email': 'email@example.com',
#             'password': 'password'
#     }

#     def setUp(self):
#         self.client = APIClient()
#         response = self.client.post('/api/account/register/', self.USER, format='json')
#         self.client.credentials(HTTP_AUTHORIZATION=f'Token {response.data["token"]}')

#         self.data = {
#             "symbol_data": {
#                 "symbol": "AAPL",
#                 "security_type": "UNDERLYING"
#             },
#             "company_name": "Apple Inc.",
#             "exchange": "NYSE",
#             "currency": "USD",
#             "industry": "Technology",
#             "description": "Description of Example Company",
#             "market_cap": 5000000,
#             "shares_outstanding": 1000000
#         }

#     def test_create_equity_valid(self):
#         response = self.client.post('/api/equities/', self.data, format='json')

#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(Equity.objects.count(), 1)
#         self.assertEqual(Equity.objects.get().company_name, 'Apple Inc.')

#     def test_create_equity_missing_data(self):
#         data = {
#             # Missing some required fields
#             "symbol_data": {
#                 "symbol": "AAPL"
#             },
#             "company_name": "Apple Inc."
#             # Missing 'exchange', 'currency', etc.
#         }
#         response = self.client.post('/api/equities/', data, format='json')
#         self.assertEqual(response.status_code, 400)  # Bad Request expected
#         self.assertIn('exchange', response.data)  # Check for error message related to missing 'exchange'

#     def test_create_equity_already_exists(self):
#         # First, create an equity
#         self.test_create_equity_valid()
#         response = self.client.post('/api/equities/', self.data, format='json')
#         self.assertNotEqual(response.status_code, 201)  # Expecting not to be 201 Created
    

#     def test_update_equity(self):
#         # First, create an equity
#         self.test_create_equity_valid()

#         # Update the equity
#         update_data = self.data
#         update_data['comapny_name'] = 'Tesla Inc.'
#         response = self.client.put('/api/equities/1/', update_data, format='json')
#         print(response)
#         self.assertEqual(response.status_code, 200)
#         # Verify the updates

#     def test_get_equity(self):
#         # First, create an equity
#         self.test_create_equity_valid()

#         # Attempt to retrieve the created equity
#         response = self.client.get('/api/equities/?symbols=AAPL/')  # Assuming URL pattern includes the symbol
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['company_name'], 'Apple Inc.')

#     def test_delete_equity(self):
#         # First, create an equity
#         self.test_create_equity_valid()

#         # Delete the equity
#         response = self.client.delete('/api/equities/AAPL/')
#         self.assertEqual(response.status_code, 204)  # No Content on successful deletion
#         # Verify it's deleted

class FutureAPITests(TestCase):
        
    USER = {
            'username': 'username',
            'email': 'email@example.com',
            'password': 'password'
    }

    def setUp(self):
        self.client = APIClient()
        response = self.client.post('/api/account/register/', self.USER, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {response.data["token"]}')

        self.data = {
            "symbol_data": {
                "symbol": "ES.n.0",
                "security_type": "FUTURE"
            },
            'contract_size', 
            'expiration_date', 
            'underlying_name',
            'base_code',
            'exchange',
            'created_at',
            'updated_at'
        }

    def test_create_equity_valid(self):
        response = self.client.post('/api/equities/', self.data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Equity.objects.count(), 1)
        self.assertEqual(Equity.objects.get().company_name, 'Apple Inc.')

    def test_create_equity_missing_data(self):
        data = {
            # Missing some required fields
            "symbol_data": {
                "symbol": "AAPL"
            },
            "company_name": "Apple Inc."
            # Missing 'exchange', 'currency', etc.
        }
        response = self.client.post('/api/equities/', data, format='json')
        self.assertEqual(response.status_code, 400)  # Bad Request expected
        self.assertIn('exchange', response.data)  # Check for error message related to missing 'exchange'

    def test_create_equity_already_exists(self):
        # First, create an equity
        self.test_create_equity_valid()
        response = self.client.post('/api/equities/', self.data, format='json')
        self.assertNotEqual(response.status_code, 201)  # Expecting not to be 201 Created
    

    def test_update_equity(self):
        # First, create an equity
        self.test_create_equity_valid()

        # Update the equity
        update_data = self.data
        update_data['comapny_name'] = 'Tesla Inc.'
        response = self.client.put('/api/equities/1/', update_data, format='json')
        print(response)
        self.assertEqual(response.status_code, 200)
        # Verify the updates

    def test_get_equity(self):
        # First, create an equity
        self.test_create_equity_valid()

        # Attempt to retrieve the created equity
        response = self.client.get('/api/equities/?symbols=AAPL/')  # Assuming URL pattern includes the symbol
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['company_name'], 'Apple Inc.')

    def test_delete_equity(self):
        # First, create an equity
        self.test_create_equity_valid()

        # Delete the equity
        response = self.client.delete('/api/equities/AAPL/')
        self.assertEqual(response.status_code, 204)  # No Content on successful deletion
        # Verify it's deleted

class OptionAPITests(TestCase):
        
    USER = {
            'username': 'username',
            'email': 'email@example.com',
            'password': 'password'
    }

    def setUp(self):
        self.client = APIClient()
        response = self.client.post('/api/account/register/', self.USER, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {response.data["token"]}')

        self.data = {
            "symbol_data": {
                "symbol": "AAPL",
                "security_type": "UNDERLYING"
            },
            "company_name": "Apple Inc.",
            "exchange": "NYSE",
            "currency": "USD",
            "industry": "Technology",
            "description": "Description of Example Company",
            "market_cap": 5000000,
            "shares_outstanding": 1000000
        }

    def test_create_equity_valid(self):
        response = self.client.post('/api/equities/', self.data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Equity.objects.count(), 1)
        self.assertEqual(Equity.objects.get().company_name, 'Apple Inc.')

    def test_create_equity_missing_data(self):
        data = {
            # Missing some required fields
            "symbol_data": {
                "symbol": "AAPL"
            },
            "company_name": "Apple Inc."
            # Missing 'exchange', 'currency', etc.
        }
        response = self.client.post('/api/equities/', data, format='json')
        self.assertEqual(response.status_code, 400)  # Bad Request expected
        self.assertIn('exchange', response.data)  # Check for error message related to missing 'exchange'

    def test_create_equity_already_exists(self):
        # First, create an equity
        self.test_create_equity_valid()
        response = self.client.post('/api/equities/', self.data, format='json')
        self.assertNotEqual(response.status_code, 201)  # Expecting not to be 201 Created
    

    def test_update_equity(self):
        # First, create an equity
        self.test_create_equity_valid()

        # Update the equity
        update_data = self.data
        update_data['comapny_name'] = 'Tesla Inc.'
        response = self.client.put('/api/equities/1/', update_data, format='json')
        print(response)
        self.assertEqual(response.status_code, 200)
        # Verify the updates

    def test_get_equity(self):
        # First, create an equity
        self.test_create_equity_valid()

        # Attempt to retrieve the created equity
        response = self.client.get('/api/equities/?symbols=AAPL/')  # Assuming URL pattern includes the symbol
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['company_name'], 'Apple Inc.')

    def test_delete_equity(self):
        # First, create an equity
        self.test_create_equity_valid()

        # Delete the equity
        response = self.client.delete('/api/equities/AAPL/')
        self.assertEqual(response.status_code, 204)  # No Content on successful deletion
        # Verify it's deleted


