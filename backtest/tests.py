import json
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from decimal import Decimal
from account.models import CustomUser
from symbols.models import Symbol, SecurityType
from market_data.models import BarData, QuoteData, Symbol
from .models import Backtest as Backtest_model

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


        # Create an asset class instance
        self.ticker="AAPL"
        self.security_type = SecurityType.objects.create(value="STOCK")
        self.symbol = Symbol.objects.create(ticker=self.ticker, security_type=self.security_type)
        self.bar_data = BarData.objects.create(symbol=self.symbol,
                                                    timestamp="2024-01-10",
                                                    open=100.99999,
                                                    high=100.99999,
                                                    low=100.99999,
                                                    close=100.99999,
                                                    volume=100.99999,
                                                    )
        
        self.backtest_data={"parameters": {
                                "strategy_name": "cointegrationzscore", 
                                "capital": 100000, 
                                "data_type": "BAR", 
                                "train_start": "2018-05-18", 
                                "train_end": "2023-01-19", 
                                "test_start": "2023-01-19", 
                                "test_end": "2024-01-19", 
                                "tickers": [self.ticker], 
                                "benchmark": ["^GSPC"]
                            },
                            "static_stats": [{
                                "net_profit": 330.0, 
                                "total_fees": 40.0, 
                                "total_return": 0.33, 
                                "ending_equity": 1330.0, 
                                "max_drawdown": 0.0, 
                                "total_trades": 2, 
                                "num_winning_trades": 2, 
                                "num_lossing_trades": 0, 
                                "avg_win_percent": 0.45, 
                                "avg_loss_percent": 0, 
                                "percent_profitable": 1.0, 
                                "profit_and_loss": 0.0, 
                                "profit_factor": 0.0, 
                                "avg_trade_profit": 165.0, 
                                "sortino_ratio": 0.0
                            }], 
                            "regression_stats": [{
                                "r_squared": "1.0", 
                                "p_value_alpha": "0.5", 
                                "p_value_beta": "0.09", 
                                "risk_free_rate": "0.01", 
                                "alpha": "16.4791", 
                                "beta": "-66.6633", 
                                "sharpe_ratio": "10.72015", 
                                "annualized_return": "39.0001", 
                                "market_contribution": "-0.498",
                                "idiosyncratic_contribution": "0.66319",
                                "total_contribution": "0.164998", 
                                "annualized_volatility": "3.7003", 
                                "market_volatility": "-0.25608",
                                "idiosyncratic_volatility": "7.85876", 
                                "total_volatility": "0.23608", 
                                "portfolio_dollar_beta": "-8862.27533", 
                                "market_hedge_nmv": "88662.2533"
                            }],
                            "timeseries_stats": [
                                {
                                    "timestamp": "2023-12-09T12:00:00Z",
                                    "equity_value": 10000.0,
                                    "percent_drawdown": 9.9, 
                                    "cumulative_return": -0.09, 
                                    "period_return": 79.9,
                                    "daily_strategy_return": "0.330", 
                                    "daily_benchmark_return": "0.00499"
                                },
                                {
                                    "timestamp": "2023-12-10T12:00:00Z",
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
                                "timestamp": "2023-01-03T00:00:00+0000", 
                                "ticker": "AAPL", 
                                "quantity": 4, 
                                "price": 130.74, 
                                "cost": -522.96, 
                                "action": "BUY", 
                                "fees": 0.0
                            }],
                            "signals": [{
                                "timestamp": "2023-01-03T00:00:00+0000", 
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
        self.assertIn('timeseries_stats', response.data)
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
                                "train_start": "2018-05-18", 
                                "train_end": "2023-01-19", 
                                "test_start": "2023-01-19", 
                                "test_end": "2024-01-19", 
                                "tickers": [self.ticker], 
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
