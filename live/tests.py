import json
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from decimal import Decimal
from account.models import CustomUser
from symbols.models import Symbol, SecurityType
from market_data.models import BarData,Symbol
from .models import LiveSession


class Base(APITestCase):
    def setUp(self):
        # Set up the client
        self.client = APIClient()

        # Set up authentication
        self.user = CustomUser.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

class LiveSessionTests(Base):
    def setUp(self):
        super().setUp()

        # url
        self.url="/api/live_session/"


        # Create an asset class instance
        self.ticker="AAPL"
        self.security_type = SecurityType.objects.create(value="STOCK")
        self.symbol = Symbol.objects.create(ticker=self.ticker, security_type=self.security_type)
        self.bar_data = BarData.objects.create(symbol=self.symbol,
                                                    timestamp=1707307740000000000,
                                                    open=100.99999,
                                                    high=100.99999,
                                                    low=100.99999,
                                                    close=100.99999,
                                                    volume=100.99999,
                                                    )
        
        self.live_session_data={"parameters": {
                                    "strategy_name": "cointegrationzscore", 
                                    "capital": 100000, 
                                    "data_type": "BAR", 
                                    "train_start": 1704862800, 
                                    "train_end": 1704893000, 
                                    "test_start": 1704903000, 
                                    "test_end": 1705903000, 
                                    "tickers": ["HE", "ZC"], 
                                    "benchmark": ["^GSPC"]
                                }, 
                                "signals": [
                                    {
                                        "timestamp": 1704903000, 
                                        "trade_instructions": [
                                            {"ticker": "HE", "order_type": "MKT", "action": "SHORT", "trade_id": 1, "leg_id": 1, "weight": "-0.8689"}, 
                                            {"ticker": "ZC", "order_type": "MKT", "action": "LONG", "trade_id": 1, "leg_id": 2, "weight": "0.1311"}
                                        ]
                                    }, 
                                    {
                                        "timestamp": 1704904000, 
                                        "trade_instructions": [
                                            {"ticker": "HE", "order_type": "MKT", "action": "SHORT", "trade_id": 1, "leg_id": 1, "weight": "-0.8689"}, 
                                            {"ticker": "ZC", "order_type": "MKT", "action": "LONG", "trade_id": 1, "leg_id": 2, "weight": "0.1311"}
                                        ]
                                    }, 
                                    {
                                        "timestamp": 1704905000, 
                                        "trade_instructions": [
                                            {"ticker": "HE", "order_type": "MKT", "action": "SHORT", "trade_id": 1, "leg_id": 1, "weight": "-0.8689"}, 
                                            {"ticker": "ZC", "order_type": "MKT", "action": "LONG", "trade_id": 1, "leg_id": 2, "weight": "0.1311"}
                                        ]
                                    }
                                ], 
                                "trades": [
                                    {
                                        "timestamp": 1704903000, 
                                        "ticker": "HE", 
                                        "quantity": 1, 
                                        "avg_price": 91.45, 
                                        "action": "SELL", 
                                        "trade_value": 948444, 
                                        "fees": 2.97,
                                    },
                                    {
                                        "timestamp": 1704904000, 
                                        "ticker": "ZC", 
                                        "quantity": 1,  
                                        "avg_price": 446.25,                                        "action": "BUY", 
                                        "trade_value": 234567, 
                                        "fees": "2.97"
                                    }
                                ], 
                                "account_data": [{
                                    "start_buying_power": "2557567.234", 
                                    "currency": "USD", 
                                    "start_excess_liquidity": "767270.345", 
                                    "start_full_available_funds": "767270.4837", 
                                    "start_full_init_margin_req": "282.3937", 
                                    "start_full_maint_margin_req": "282.3938", 
                                    "start_futures_pnl": "-464.883", 
                                    "start_net_liquidation": "767552.392", 
                                    "start_total_cash_balance": "-11292.332", 
                                    "start_unrealized_pnl": "0", 
                                    "start_timestamp": 1704903000, 
                                    "end_buying_power": "2535588.9282", 
                                    "end_excess_liquidity": "762034.2928", 
                                    "end_full_available_funds": "760676.292", 
                                    "end_full_init_margin_req": "7074.99", 
                                    "end_full_maint_margin_req": "5716.009", 
                                    "end_futures_pnl": "-487.998", 
                                    "end_net_liquidation": "767751.998", 
                                    "end_total_cash_balance": "766935.99", 
                                    "end_unrealized_pnl": "-28.99", 
                                    "end_timestamp": 1704904000
                                }]
                            }
        
        response = self.client.post(self.url, data=self.live_session_data, format='json')
        self.live_session_id = response.data['id']

    def test_get_live_session_list(self):
        # test
        response = self.client.get(self.url)

        # validate
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.data[0])
        self.assertIn('strategy_name', response.data[0])
        self.assertIn('tickers', response.data[0])
        self.assertIn('benchmark', response.data[0])
        self.assertIn('data_type', response.data[0])
        self.assertIn('train_start', response.data[0])
        self.assertIn('test_start', response.data[0])
        self.assertIn('capital', response.data[0])

    def test_get_live_session_by_id(self):
        url = f"{self.url}{self.live_session_id}/"
        # test
        response = self.client.get(url)

        # validate
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.data)
        self.assertIn('parameters', response.data)
        self.assertIn('signals', response.data)
        self.assertIn('trades', response.data)
        self.assertIn('account_data', response.data)

    def test_create_live_session(self):
        # test
        response = self.client.post(self.url, data=self.live_session_data, format='json')

        # validate
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LiveSession.objects.count(), 2)

    def test_delete_live_session(self):
        url = f"{self.url}{self.live_session_id}/"
        
        # test
        response = self.client.delete(url)

        # validate
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(LiveSession.objects.count(), 0)

    def test_update_live_session(self):
        data = {
                "parameters": {
                                "strategy_name": "cnothing", 
                                "capital": 100000, 
                                "data_type": "BAR", 
                                "train_start": 1704862800, 
                                "train_end": 1704893000, 
                                "test_start": 1704903000, 
                                "test_end": 1705903000, 
                                "tickers": [self.ticker], 
                                "benchmark": ["XXXt"]
                            }
        }

        url = f"{self.url}{self.live_session_id}/"

        # test
        response = self.client.patch(url, data, format='json')

        # validate
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(LiveSession.objects.count(), 1)
        self.assertEqual(LiveSession.objects.last().benchmark, ["XXXt"])
