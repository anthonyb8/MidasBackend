import json
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from account.models import CustomUser
from .models import Backtest as Backtest_model
from symbols.models import Symbol, SecurityType
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from market_data.models import BarData, QuoteData, Symbol

# TODO: test options/cryptocurrency models

class Base(APITestCase):
    def setUp(self):
        # Set up the client
        self.client = APIClient()

        # Set up authentication
        self.user = CustomUser.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

class Backtest(Base):
    def setUp(self):
        super().setUp()

        # url
        self.url="/api/backtest/"

        # # Create an asset class instance
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
        
        self.backtest_data={
                            "parameters": {
                                "strategy_name": "cointegrationzscore", 
                                "capital": 100000, 
                                "data_type": "BAR", 
                                "train_start": 1704862800, 
                                "train_end": 1704893000, 
                                "test_start": 1704903000, 
                                "test_end": 1705903000, 
                                "tickers": ['AAPL'], 
                                "benchmark": ["^GSPC"]
                            },
                            "static_stats": [{
                                "net_profit": 330.0, 
                                "total_fees": 40.0, 
                                "ending_equity": 1330.0, 
                                "avg_trade_profit": 165.0, 
                                "total_return": 0.33, 
                                "annual_standard_deviation_percentage": 0.23, 
                                "max_drawdown_percentage": 0.0, 
                                "avg_win_percentage": 0.45, 
                                "avg_loss_percentage": 0, 
                                "percent_profitable": 1.0, 
                                "total_trades": 2, 
                                "number_winning_trades": 2, 
                                "number_losing_trades": 0, 
                                "profit_and_loss_ratio": 0.0, 
                                "profit_factor": 0.0, 
                                "sortino_ratio": 0.0,
                                "sharpe_ratio": 10.72015,
                            }],
                            "period_timeseries_stats": [
                                {
                                    "timestamp": 1704903000,
                                    "equity_value": 10000.0,
                                    "percent_drawdown": 9.9, 
                                    "cumulative_return": -0.09, 
                                    "period_return": 79.9,
                                    "daily_strategy_return": "0.330", 
                                    "daily_benchmark_return": "0.00499"
                                },
                                {
                                    "timestamp": 1704904000,
                                    "equity_value": 10000.0,
                                    "percent_drawdown": 9.9, 
                                    "cumulative_return": -0.09, 
                                    "period_return": 79.9,
                                    "daily_strategy_return": "0.087", 
                                    "daily_benchmark_return": "0.009"
                                }
                            ],
                            "daily_timeseries_stats": [
                                {
                                    "timestamp": 1704903000,
                                    "equity_value": 10000.0,
                                    "percent_drawdown": 9.9, 
                                    "cumulative_return": -0.09, 
                                    "period_return": 79.9,
                                    "daily_strategy_return": "0.330", 
                                    "daily_benchmark_return": "0.00499"
                                },
                                {
                                    "timestamp": 1704904000,
                                    "equity_value": 10000.0,
                                    "percent_drawdown": 9.9, 
                                    "cumulative_return": -0.09, 
                                    "period_return": 79.9,
                                    "daily_strategy_return": "0.087", 
                                    "daily_benchmark_return": "0.009"
                                }
                            ],
                            "trades": [{
                                "trade_id": 1, 
                                "leg_id": 1, 
                                "timestamp": 1704903000, 
                                "ticker": "AAPL", 
                                "quantity": 4, 
                                "price": 130.74, 
                                "cost": -522.96, 
                                "action": "BUY", 
                                "fees": 0.0
                            }],
                            "signals": [{
                                "timestamp": 1704903000, 
                                "trade_instructions": [{
                                    "ticker": "AAPL", 
                                    "action": "BUY", 
                                    "trade_id": 1, 
                                    "leg_id": 1, 
                                    "weight": 0.05
                                }, 
                                {
                                    "ticker": "MSFT", 
                                    "action": "SELL", 
                                    "trade_id": 1, 
                                    "leg_id": 2, 
                                    "weight": 0.05
                                }]
                            }]
                            }
        response = self.client.post(self.url, data=self.backtest_data, format='json')
        self.backtest_id = response.data['id']

    def test_get_backtest_list(self):
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

    def test_get_backtest_by_id(self):
        url = f"{self.url}{self.backtest_id}/"
        # test
        response = self.client.get(url)

        # validate
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.data)
        self.assertIn('parameters', response.data)
        self.assertIn('static_stats', response.data)
        self.assertIn('period_timeseries_stats', response.data)
        self.assertIn('daily_timeseries_stats', response.data)
        self.assertIn('signals', response.data)
        self.assertIn('trades', response.data)
        self.assertIn('regression_stats', response.data)

    def test_create_backtest(self):
        # test
        response = self.client.post(self.url, data=self.backtest_data, format='json')

        # validate
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Backtest_model.objects.count(), 2)

    def test_delete_backtest(self):
        url = f"{self.url}{self.backtest_id}/"
        
        # test
        response = self.client.delete(url)

        # validate
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Backtest_model.objects.count(), 0)

    def test_update_backtest(self):
        data = {
                "parameters": {
                                "strategy_name": "cnothing", 
                                "capital": 100000, 
                                "data_type": "BAR", 
                                "train_start": 1704862800, 
                                "train_end": 1704893000, 
                                "test_start": 1704903000, 
                                "test_end": 1705903000, 
                                "tickers": ['AAPL'], 
                                "benchmark": ["XXXt"]
                            }
        }

        url = f"{self.url}{self.backtest_id}/"

        # test
        response = self.client.patch(url, data, format='json')

        # validate
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Backtest_model.objects.count(), 1)
        self.assertEqual(Backtest_model.objects.last().benchmark, ["XXXt"])
