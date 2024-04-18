import json
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from decimal import Decimal
from account.models import CustomUser
from symbols.models import Symbol, SecurityType
from market_data.models import BarData,Symbol
from .models import Session, Position, Account, Order, Risk, MarketData

#TODO: Risk and MarketData

class Base(APITestCase):
    def setUp(self):
        # Set up the client
        self.client = APIClient()

        # Set up authentication
        self.user = CustomUser.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

class SessionViewSetTests(Base):
    def setUp(self):
        super().setUp()

        # url
        self.url="/api/sessions/"

        # session
        self.session= Session.objects.create(session_id=1)
        
        # position
        self.positon_data = {
                            "data" : {
                                "action" : "BUY",
                                "avg_cost" : 150,
                                "quantity" : 100,
                                "total_cost" : 15000.00,
                                "market_value" : 160000.11,
                                "multiplier" : 1, 
                                "initial_margin" : 0.0,
                                "ticker" : "AAPL",
                                "price" : 160
                            }
        }
        self.position = self.client.post(f"{self.url}{self.session.session_id}/positions/", data=self.positon_data, format='json')

        # account
        self.account_data ={
            "data" : {
                "Timestamp" : "2024-01-01",
                "FullAvailableFunds" : 1000.99,
                "FullInitMarginReq" : 99980.99,
                "NetLiquidation" : 99.98,
                "UnrealizedPnL" : 1000.9,
                "FullMaintMarginReq" : 86464.39,
                "ExcessLiquidity" : 99333.99,
                "Currency" : "USD",
                "BuyingPower" : 777.89,
                "FuturesPNL" : 564837.99,
                "TotalCashBalance" : 999.99
            }
        }
        self.account = self.client.post(f"{self.url}{self.session.session_id}/account/", data=self.positon_data, format='json')

        # orders
        self.order_data ={
                            "data" : {
                                "permId" : 1,
                                "clientId" : 22,
                                "orderId" : 5,
                                "parentId" : 5,
                                "account": "DU12546",
                                "symbol" : "AAPL",
                                "secType" : "STK",
                                "exchange": "NASDAQ",
                                "action" : "BUY",
                                "orderType" : "MKT",
                                "totalQty" : 1009.90,
                                "cashQty" : 109.99,
                                "lmtPrice" : 0.0,
                                "auxPrice" : 0.0,
                                "status" : "Submitted",
                                "filled" : "9",
                                "remaining" : 10,
                                "avgFillPrice" : 100, 
                                "lastFillPrice": 100,
                                "whyHeld" : "",
                                "mktCapPrice" : 1000.99
                            }
        }
        self.order = self.client.post(f"{self.url}{self.session.session_id}/orders/", data=self.positon_data, format='json')

        # url
        self.url="/api/sessions/"

    def test_get_live_session_list(self):
        # test
        response = self.client.get(self.url)

        # validate
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['session_id'], 1)

    def test_get_live_session_by_id(self):
        url = f"{self.url}{self.session.session_id}/"
        
        # test
        response = self.client.get(url)

        # validate
        self.assertEqual(response.status_code, 200)
        self.assertIn('positions', response.data)
        self.assertIn('account', response.data)
        self.assertIn('orders', response.data)
        self.assertIn('risk', response.data)
        self.assertIn('market_data', response.data)

    def test_create_live_session(self):
        data = {"session_id": 2}

        # test
        response = self.client.post(self.url, data, format='json')

        # validate
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Session.objects.count(), 2)

    def test_delete_live_session(self):
        url = f"{self.url}{self.session.session_id}/"
        
        # test
        response = self.client.delete(url)

        # validate
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Session.objects.count(), 0)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Position.objects.count(), 0)
        self.assertEqual(Account.objects.count(), 0)
    
    def test_get_positions(self):
        url = f"{self.url}{self.session.session_id}/positions/"

        # test 
        response=self.client.get(url)
        
        
        # validate
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.session.session_id)

    def test_create_position(self):
        data = {"session_id": 2}
        response = self.client.post(self.url, data, format='json')

        # test
        url = f"{self.url}2/positions/"
        response= self.client.post(f"{url}", data=self.positon_data, format='json')

        # validate
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Position.objects.count(), 2)
        self.assertEqual(response.data['id'], 2)

    def test_delete_positiom(self):
        url = f"{self.url}{self.session.session_id}/positions/"
        
        # test
        response = self.client.delete(url)

        # validate
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Session.objects.count(), 1)
        self.assertEqual(Position.objects.count(), 0)

    def test_update_position(self):
        positon_data = {"data" : {
                                    "action" : "SELL",
                                    "avg_cost" : 150,
                                    "quantity" : 100,
                                    "total_cost" : 15000.00,
                                    "market_value" : 160000.11,
                                    "multiplier" : 1, 
                                    "initial_margin" : 0.0,
                                    "ticker" : "AAPL",
                                    "price" : 160
                                }
                        }
        # test
        url = f"{self.url}{self.session.session_id}/positions/"
        response = self.client.patch(url, data=positon_data, format='json')

        # validate
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Position.objects.count(), 1)
        self.assertEqual(Position.objects.last().data["action"], "SELL")
    
    def test_get_orders(self):
        url = f"{self.url}{self.session.session_id}/orders/"

        # test 
        response=self.client.get(url)
        
        # validate
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.session.session_id)

    def test_create_orders(self):
        data = {"session_id": 2}
        response = self.client.post(self.url, data, format='json')

        # test
        url = f"{self.url}2/orders/"
        response= self.client.post(f"{url}", data=self.order_data, format='json')

        # validate
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(response.data['id'], 2)

    def test_delete_orders(self):
        url = f"{self.url}{self.session.session_id}/orders/"
        
        # test
        response = self.client.delete(url)

        # validate
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Session.objects.count(), 1)
        self.assertEqual(Order.objects.count(), 0)
    
    def test_update_orders(self):
        order_data ={"data" : {
                                "permId" : 1,
                                "clientId" : 22,
                                "orderId" : 5,
                                "parentId" : 5,
                                "account": "DU12546",
                                "symbol" : "AAPL",
                                "secType" : "STK",
                                "exchange": "NASDAQ",
                                "action" : "SELL",
                                "orderType" : "MKT",
                                "totalQty" : 1009.90,
                                "cashQty" : 109.99,
                                "lmtPrice" : 0.0,
                                "auxPrice" : 0.0,
                                "status" : "Submitted",
                                "filled" : "9",
                                "remaining" : 10,
                                "avgFillPrice" : 100, 
                                "lastFillPrice": 100,
                                "whyHeld" : "",
                                "mktCapPrice" : 1000.99
                            }
        }
        # test
        url = f"{self.url}{self.session.session_id}/orders/"
        response = self.client.patch(url, data=order_data, format='json')

        # validate
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.last().data["action"], "SELL")
    
    def test_get_account(self):
        url = f"{self.url}{self.session.session_id}/account/"

        # test 
        response=self.client.get(url)
        
        # validate
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.session.session_id)

    def test_create_account(self):
        data = {"session_id": 2}
        response = self.client.post(self.url, data, format='json')

        # test
        url = f"{self.url}2/account/"
        response= self.client.post(f"{url}", data=self.positon_data, format='json')

        # validate
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(response.data['id'], 2)

    def test_delete_account(self):
        url = f"{self.url}{self.session.session_id}/account/"
        
        # test
        response = self.client.delete(url)

        # validate
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Session.objects.count(), 1)
        self.assertEqual(Account.objects.count(), 0)
    
    def test_update_account(self):
        account_data ={
            "data" : {
                "Timestamp" : "2024-01-01",
                "FullAvailableFunds" : 777777,
                "FullInitMarginReq" : 99980.99,
                "NetLiquidation" : 99.98,
                "UnrealizedPnL" : 1000.9,
                "FullMaintMarginReq" : 86464.39,
                "ExcessLiquidity" : 99333.99,
                "Currency" : "USD",
                "BuyingPower" : 777.89,
                "FuturesPNL" : 564837.99,
                "TotalCashBalance" : 999.99
            }
        }
        # test
        url = f"{self.url}{self.session.session_id}/account/"
        response = self.client.patch(url, data=account_data, format='json')

        # validate
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.last().data["FullAvailableFunds"], 777777)
    
