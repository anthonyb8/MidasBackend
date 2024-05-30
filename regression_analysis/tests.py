import json
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from account.models import CustomUser
from .models import RegressionAnalysis
from symbols.models import Symbol, SecurityType
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from market_data.models import BarData, QuoteData, Symbol

class Base(APITestCase):
    def setUp(self):
        # Set up the client
        self.client = APIClient()

        # Set up authentication
        self.user = CustomUser.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

class Regression(Base):
    def setUp(self):
        super().setUp()

        # url
        self.url="/api/regression_analysis/"

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
        self.backtest_data={
                            "parameters": {
                                "strategy_name": "cointegrationzscore", 
                                "capital": 100000, 
                                "data_type": "BAR", 
                                "train_start": 1704862800, 
                                "train_end": 1704893000, 
                                "test_start": 1704903000, 
                                "test_end": 1705903000, 
                                "tickers": [self.ticker], 
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

        response = self.client.post("/api/backtest/", data=self.backtest_data, format='json')
        self.backtest_id = response.data['id']

        # Mock Data
        self.regression_data={
                                "backtest":self.backtest_id,
                                "r_squared": "1.0", 
                                "p_value_alpha": "0.5", 
                                "p_value_beta": "0.09", 
                                "risk_free_rate": "0.01", 
                                "alpha": "16.4791", 
                                "beta": "-66.6633", 
                                # "annualized_return": "39.0001", 
                                "market_contribution": "-0.498",
                                "idiosyncratic_contribution": "0.66319",
                                "total_contribution": "0.164998", 
                                # "annualized_volatility": "3.7003", 
                                "market_volatility": "-0.25608",
                                "idiosyncratic_volatility": "7.85876", 
                                "total_volatility": "0.23608", 
                                "portfolio_dollar_beta": "-8862.27533", 
                                "market_hedge_nmv": "88662.2533"
                            }
        
    def test_create(self):
        # test
        response = self.client.post(self.url, data=self.regression_data, format='json')

        # validate
        self.assertEqual(response.status_code, 201)
        self.assertEqual(RegressionAnalysis.objects.count(), 1)

    def test_create_duplicate(self):
        # set-up
        self.client.post(self.url, data=self.regression_data, format='json')

        # test
        with self.assertRaises(Exception):
            response = self.client.post(self.url, data=self.regression_data, format='json')

    def test_get(self):
        # set-up
        self.client.post(self.url, data=self.regression_data, format='json')
        url = f"{self.url}{self.backtest_id}/"

        # test
        response = self.client.get(url)

        # validate
        self.assertEqual(response.status_code, 200)
        self.assertIn('backtest', response.data)
        self.assertIn('r_squared', response.data)
        self.assertIn('alpha', response.data)
        self.assertIn('p_value_alpha', response.data)
        self.assertIn('beta', response.data)
        self.assertIn('p_value_beta', response.data)
        self.assertIn('risk_free_rate', response.data)
        self.assertIn('market_contribution', response.data)
        self.assertIn('idiosyncratic_contribution', response.data)
        self.assertIn('market_volatility', response.data)
        self.assertIn('idiosyncratic_volatility', response.data)
        self.assertIn('total_volatility', response.data)
        self.assertIn('portfolio_dollar_beta', response.data)
        self.assertIn('market_hedge_nmv', response.data)

    def test_delete(self):
        # set-up
        self.client.post(self.url, data=self.regression_data, format='json')
        url = f"{self.url}{self.backtest_id}/"

        # test
        response = self.client.delete(url)

        # validate
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RegressionAnalysis.objects.count(), 0)

    def test_update(self):
        # set-up
        self.client.post(self.url, data=self.regression_data, format='json')
        url = f"{self.url}{self.backtest_id}/"
        updated_alpha = 100.00
        self.regression_data["alpha"] = updated_alpha

        # test
        response = self.client.put(url, data=self.regression_data, format='json')

        # validate
        self.assertEqual(response.status_code, 200)
        self.assertIn('backtest', response.data)
        self.assertIn('r_squared', response.data)
        self.assertEqual(response.data['alpha'],"100.00000000")



    