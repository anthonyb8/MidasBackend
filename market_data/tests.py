import json
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from decimal import Decimal
from account.models import CustomUser
from symbols.models import Symbol, SecurityType
from .models import BarData, QuoteData, Symbol

# TODO: test options/cryptocurrency models

class Base(APITestCase):
    def setUp(self):
        # Set up the client
        self.client = APIClient()

        # Set up authentication
        self.user = CustomUser.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

class BarDataViewSetTest(Base):
    def setUp(self):
        super().setUp()

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
        # URL for the asset class endpoint
        self.url = '/api/bardata/'

    def test_list_all_bar_data(self):
        # test
        response = self.client.get(self.url)
        
        # validate
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['symbol'], self.ticker)
    
    def test_get_bar_data_by_tickers(self):
        ticker="MSFT"
        symbol = Symbol.objects.create(ticker=ticker, security_type=self.security_type)
        bar_data = BarData.objects.create(symbol=symbol,
                                                    timestamp=1707307740000000000,
                                                    open=100.99999,
                                                    high=100.99999,
                                                    low=100.99999,
                                                    close=100.99999,
                                                    volume=100.99999,
                                                    )
        url = f"{self.url}?tickers=AAPL,MSFT"

        # test
        response=self.client.get(url)

        # validate
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 1)
        self.assertEqual(response.data[0]['symbol'], self.ticker)
        self.assertEqual(response.data[1]['symbol'], ticker)

    def test_get_bar_data_by_ticker_and_date_range(self):
        bar_data = BarData.objects.create(symbol=self.symbol,
                                                    timestamp=1707307750000000000,
                                                    open=100.99999,
                                                    high=100.99999,
                                                    low=100.99999,
                                                    close=100.99999,
                                                    volume=100.99999,
                                                    )
        url = f"{self.url}?tickers=AAPL&start_date=1707307740000000000&end_date=1707307760000000000"

        # test
        response=self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['symbol'], self.ticker)
        self.assertEqual(response.data[1]['symbol'], self.ticker)

    def test_create_bar_data(self):
        ticker="F"
        symbol = Symbol.objects.create(ticker=ticker, security_type=self.security_type)

        data= {
            "symbol":ticker,    
            "timestamp":1707307740000000000,
            "open":100.9999,
            "high":100.9999,
            "low":100.9999,
            "close":100.9999,    
            "volume":100,

        }

        # test
        response = self.client.post(self.url, data, format='json')

        # validate
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BarData.objects.count(), 2)
        self.assertEqual(BarData.objects.last().symbol.ticker, 'F')

    def test_bulk_create_bar_data(self):
        ticker="F"
        symbol = Symbol.objects.create(ticker=ticker, security_type=self.security_type)

        data= [{
            "symbol":ticker,    
            "timestamp":1707307750000000000,
            "open":100.9999,
            "high":100.9999,
            "low":100.9999,
            "close":100.9999,    
            "volume":100,

        },{
            "symbol":ticker,    
            "timestamp":1707307760000000000,
            "open":99.9999,
            "high":100.9999,
            "low":100.9999,
            "close":100.9999,    
            "volume":100
        }]

        url=f"{self.url}bulk_create/"

        # test
        response = self.client.post(url, data, format='json')

        # validate
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BarData.objects.count(), 3)
        self.assertEqual(BarData.objects.last().symbol.ticker, 'F')
        self.assertEqual(BarData.objects.last().open, Decimal('99.9999'))

    def test_bulk_create_with_overlap(self):
        data= [{
            "symbol":self.ticker,    
            "timestamp":1707307740000000000,
            "open":99.9999,
            "high":99.9999,
            "low":99.9999,
            "close":99.9999,    
            "volume":99999,

        },{
            "symbol":self.ticker,    
            "timestamp":1707307750000000000,
            "open":99.9999,
            "high":100.9999,
            "low":100.9999,
            "close":100.9999,    
            "volume":100
        }]

        url=f"{self.url}bulk_create/"

        # test
        response = self.client.post(url, data, format='json')

        # validate
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BarData.objects.count(), 2)
        self.assertEqual(len(response.data['errors']), 1)
        self.assertEqual(len(response.data['created']), 1)

    def test_update_bar_data(self):

        data= {
            "symbol":self.ticker,    
            "timestamp":1707307740000000000,
            "open":100.9999,
            "high":100.9999,
            "low":100.9999,
            "close":100.9999,    
            "volume":99999,

        }


        url = f"{self.url}{self.bar_data.id}/"
        # test
        response = self.client.put(url, data)

        # validate
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.bar_data.refresh_from_db()
        self.assertEqual(self.bar_data.volume, 99999)

    def test_delete_bar_data(self):
        url = f"{self.url}{self.bar_data.id}/"

        # test
        response = self.client.delete(url)

        # validate
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BarData.objects.count(), 0)

    def test_delete_symbol_cascade(self):
        url = f"/api/symbols/{self.symbol.id}/"
        
        # test
        response = self.client.delete(url)
        
        # validate
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BarData.objects.count(), 0)

class QuoteDataViewSetTest(Base):
    def setUp(self):
        super().setUp()

        # Create an asset class instance
        self.ticker="AAPL"
        self.security_type = SecurityType.objects.create(value="STOCK")
        self.symbol = Symbol.objects.create(ticker=self.ticker, security_type=self.security_type)
        self.quote_data = QuoteData.objects.create(symbol=self.symbol,
                                                    timestamp=1704862800,
                                                    ask=90.999,
                                                    ask_size=9849.999,
                                                    bid=89.99,
                                                    bid_size=9990.8778
                                                    )
        # URL for the asset class endpoint
        self.url = '/api/quotedata/'

    def test_list_all_quote_data(self):
        # test
        response = self.client.get(self.url)
        
        # validate
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['symbol'], self.ticker)
    
    def test_get_quote_data_by_tickers(self):
        ticker="MSFT"
        symbol = Symbol.objects.create(ticker=ticker, security_type=self.security_type)
        quote_data = QuoteData.objects.create(symbol=symbol,
                                                    timestamp=1704862800,
                                                    ask=90.999,
                                                    ask_size=9849.999,
                                                    bid=89.99,
                                                    bid_size=9990.8778
                                                    )
        url = f"{self.url}?tickers=AAPL,MSFT"

        # test
        response=self.client.get(url)

        # validate
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 1)
        self.assertEqual(response.data[0]['symbol'], self.ticker)
        self.assertEqual(response.data[1]['symbol'], ticker)

    def test_get_quote_data_by_ticker_and_date_range(self):
        quote_data = QuoteData.objects.create(symbol=self.symbol,
                                                    timestamp=1704862900,
                                                    ask=90.999,
                                                    ask_size=9849.999,
                                                    bid=89.99,
                                                    bid_size=9990.8778
                                                    )
        url = f"{self.url}?tickers=AAPL&start_date=1704862800&end_date=1704863000"

        # test
        response=self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['symbol'], self.ticker)
        self.assertEqual(response.data[1]['symbol'], self.ticker)

    def test_create_quote_data(self):
        ticker="F"
        symbol = Symbol.objects.create(ticker=ticker, security_type=self.security_type)

        data= {
            "symbol":ticker,    
            "timestamp":1704862800,
            "ask":90.999,
            "ask_size":9849.999,
            "bid":89.99,
            "bid_size":9990.8778
        }

        # test
        response = self.client.post(self.url, data, format='json')

        # validate
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(QuoteData.objects.count(), 2)
        self.assertEqual(QuoteData.objects.last().symbol.ticker, 'F')

    def test_bulk_create_quote_data(self):
        ticker="F"
        symbol = Symbol.objects.create(ticker=ticker, security_type=self.security_type)

        data= [{
            "symbol":ticker,    
            "timestamp":1704862800,
            "ask":90.999,
            "ask_size":9849.999,
            "bid":89.99,
            "bid_size":9990.8778

        },{
            "symbol":ticker,    
            "timestamp":1704862900,
            "ask":90.999,
            "ask_size":9849.999,
            "bid":89.99,
            "bid_size":9990.8778
        }]

        url=f"{self.url}bulk_create/"

        # test
        response = self.client.post(url, data, format='json')

        # validate
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(QuoteData.objects.count(), 3)
        self.assertEqual(QuoteData.objects.last().symbol.ticker, 'F')
        self.assertEqual(QuoteData.objects.last().ask, Decimal('90.999'))

    def test_bulk_create_with_overlap(self):
        data= [{
            "symbol":self.ticker,    
            "timestamp":1704862800,
            "ask":111.999,
            "ask_size":111.999,
            "bid":111.99,
            "bid_size":1111.8778

        },{
            "symbol":self.ticker,    
            "timestamp":1704862900,
            "ask":90.999,
            "ask_size":9849.999,
            "bid":89.99,
            "bid_size":9990.8778
        }]

        url=f"{self.url}bulk_create/"

        # test
        response = self.client.post(url, data, format='json')

        # validate
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(QuoteData.objects.count(), 2)
        self.assertEqual(len(response.data['errors']), 1)
        self.assertEqual(len(response.data['created']), 1)

    def test_update_quote_data(self):
        data= {
            "symbol":self.ticker,    
            "timestamp":1704862800,
            "ask":111.999,
            "ask_size":111.999,
            "bid":1234.99,
            "bid_size":91234.8778

        }


        url = f"{self.url}{self.quote_data.id}/"
        # test
        response = self.client.put(url, data)

        # validate
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.quote_data.refresh_from_db()
        self.assertEqual(self.quote_data.ask, Decimal('111.999'))

    def test_delete_quote_data(self):
        url = f"{self.url}{self.quote_data.id}/"

        # test
        response = self.client.delete(url)

        # validate
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(QuoteData.objects.count(), 0)

    def test_delete_symbol_cascade(self):
        url = f"/api/symbols/{self.symbol.id}/"
        
        # test
        response = self.client.delete(url)
        
        # validate
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(QuoteData.objects.count(), 0)
