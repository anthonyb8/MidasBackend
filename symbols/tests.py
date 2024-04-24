
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from account.models import CustomUser
from .models import (AssetClass, Currency, SecurityType, ContractUnits, Venue, Industry,
                    Symbol, Equity, Option, Future, Cryptocurrency, Index)

# TODO: test options/cryptocurrency models

class Base(APITestCase):
    def setUp(self):
        # Set up the client
        self.client = APIClient()

        # Set up authentication
        self.user = CustomUser.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

# -- Symbol Details --
class AssetClassViewSetTest(Base):
    def setUp(self):
        super().setUp()

        # Create an asset class instance
        self.asset_class = AssetClass.objects.create(value="EQUITY")
        # URL for the asset class endpoint
        self.url = '/api/asset_class/'

    def test_list_asset_classes(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['value'], 'EQUITY')

    def test_create_asset_class(self):
        response = self.client.post(self.url, {'value': 'COMMODITY'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AssetClass.objects.count(), 2)
        self.assertEqual(AssetClass.objects.last().value, 'COMMODITY')

    def test_update_asset_class(self):
        url = f"{self.url}{self.asset_class.id}/"
        response = self.client.patch(url, {'value': 'FIXED INCOME'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.asset_class.refresh_from_db()
        self.assertEqual(self.asset_class.value, 'FIXED INCOME')


    def test_delete_asset_class(self):
        # detail_url = reverse('assetclass-detail', args=[self.asset_class.id])
        url = f"{self.url}{self.asset_class.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AssetClass.objects.count(), 0)

class CurrencyViewSetTest(Base):
    def setUp(self):
        super().setUp()
        self.currency = Currency.objects.create(value="USD")
        self.url = '/api/currency/'  # Adjust the URL based on your actual API endpoint

    def test_list_currencies(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['value'], 'USD')

    def test_create_currency(self):
        response = self.client.post(self.url, {'value': 'EUR'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Currency.objects.count(), 2)
        self.assertEqual(Currency.objects.last().value, 'EUR')

    def test_update_currency(self):
        url = f"{self.url}{self.currency.id}/"
        response = self.client.patch(url, {'value': 'GBP'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.currency.refresh_from_db()
        self.assertEqual(self.currency.value, 'GBP')

    def test_delete_currency(self):
        url = f"{self.url}{self.currency.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Currency.objects.count(), 0)

class SecurityTypeViewSetTest(Base):
    def setUp(self):
        super().setUp()
        self.security_type = SecurityType.objects.create(value="FUTURE")
        self.url = '/api/security_type/'  # Adjust the URL based on your actual API endpoint

    def test_list_security_types(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['value'], 'FUTURE')

    def test_create_security_type(self):
        response = self.client.post(self.url, {'value': 'STOCK'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SecurityType.objects.count(), 2)
        self.assertEqual(SecurityType.objects.last().value, 'STOCK')

    def test_update_security_type(self):
        url = f"{self.url}{self.security_type.id}/"
        response = self.client.patch(url, {'value': 'FOREX'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.security_type.refresh_from_db()
        self.assertEqual(self.security_type.value, 'FOREX')

    def test_delete_security_type(self):
        url = f"{self.url}{self.security_type.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SecurityType.objects.count(), 0)

class VenueViewSetTest(Base):
    def setUp(self):
        super().setUp()
        self.venue = Venue.objects.create(value="CME")
        self.url = '/api/venue/'  # Adjust the URL based on your actual API endpoint

    def test_list_venues(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['value'], 'CME')

    def test_create_venue(self):
        response = self.client.post(self.url, {'value': 'NASDAQ'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Venue.objects.count(), 2)
        self.assertEqual(Venue.objects.last().value, 'NASDAQ')

    def test_update_venue(self):
        url = f"{self.url}{self.venue.id}/"
        response = self.client.patch(url, {'value': 'NYSE'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.venue.refresh_from_db()
        self.assertEqual(self.venue.value, 'NYSE')

    def test_delete_venue(self):
        url = f"{self.url}{self.venue.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Venue.objects.count(), 0)

class IndustryViewSetTest(Base):
    def setUp(self):
        super().setUp()
        self.industry = Industry.objects.create(value="Technology")
        self.url = '/api/industry/'  # Adjust the URL based on your actual API endpoint

    def test_list_industrys(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['value'], 'Technology')

    def test_create_industry(self):
        response = self.client.post(self.url, {'value': 'Metals'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Industry.objects.count(), 2)
        self.assertEqual(Industry.objects.last().value, 'Metals')

    def test_update_industry(self):
        url = f"{self.url}{self.industry.id}/"
        response = self.client.patch(url, {'value': 'Materials'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.industry.refresh_from_db()
        self.assertEqual(self.industry.value, 'Materials')

    def test_delete_industry(self):
        url = f"{self.url}{self.industry.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Industry.objects.count(), 0)

class ContractUnitsViewSetTest(Base):
    def setUp(self):
        super().setUp()
        self.contract_units = ContractUnits.objects.create(value="Bushels")
        self.url = '/api/contract_units/'  # Adjust the URL based on your actual API endpoint

    def test_list_contract_unitss(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['value'], 'Bushels')

    def test_create_contract_units(self):
        response = self.client.post(self.url, {'value': 'Barrels'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContractUnits.objects.count(), 2)
        self.assertEqual(ContractUnits.objects.last().value, 'Barrels')

    def test_update_contract_units(self):
        url = f"{self.url}{self.contract_units.id}/"
        response = self.client.patch(url, {'value': 'Pounds'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contract_units.refresh_from_db()
        self.assertEqual(self.contract_units.value, 'Pounds')

    def test_delete_contract_units(self):
        url = f"{self.url}{self.contract_units.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ContractUnits.objects.count(), 0)

# -- Symbols --
class SymbolTestWithEquity(Base):
    def setUp(self):
        super().setUp()
        
        # Set up required objects
        self.security_type = SecurityType.objects.create(value="STK")
        self.venue = Venue.objects.create(value="NASDAQ")
        self.industry = Industry.objects.create(value="Technology")
        self.currency = Currency.objects.create(value="USD")
        self.symbol = Symbol.objects.create(ticker="AAPL", security_type=self.security_type)

        # URLs
        self.url = "/api/symbols/"

    def test_get_symbol_by_ticker(self):
        response = self.client.get(self.url, {'ticker': 'AAPL'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['ticker'], 'AAPL')

    def test_create_symbol_with_equity(self):
        data = {
            'ticker': 'GOOGL',
            'security_type': self.security_type.value,
            'symbol_data': {
                            'company_name': "Google", 
                            'venue': self.venue.value, 
                            'currency': self.currency.value,
                            'industry': self.industry.value,
                            'market_cap': 2000000,
                            'shares_outstanding': 9000000,
                            }
        }
        
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Symbol.objects.count(), 2)
        self.assertEqual(Equity.objects.count(), 1)
        self.assertEqual(Equity.objects.last().company_name, 'Google')

    def test_delete_symbol_with_equity(self):
        symbol = Symbol.objects.create(ticker="TTV", security_type=self.security_type)
        equity = Equity.objects.create(symbol=symbol, company_name="Google", venue=self.venue, 
                                       currency=self.currency, industry=self.industry,market_cap=10000000,
                                       shares_outstanding=90909090)

        url = f"{self.url}{symbol.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Symbol.objects.count(), 1)
        self.assertEqual(Equity.objects.count(), 0)

    def test_update_symbol_with_equity(self):
        symbol = Symbol.objects.create(ticker="TTV", security_type=self.security_type)
        equity = Equity.objects.create(symbol=symbol, company_name="Google", venue=self.venue, 
                                       currency=self.currency, industry=self.industry,market_cap=10000000,
                                       shares_outstanding=90909090)
        data = {
            'ticker': 'TELE',
            'security_type': self.security_type.value,
            'symbol_data': {
                            'company_name': "UpdatedGoogle", 
                            'venue': self.venue.value, 
                            'currency': self.currency.value,
                            'industry': self.industry.value,
                            'market_cap': 2000000,
                            'shares_outstanding': 9000000,
                            }
            }
        url = f"{self.url}{symbol.id}/"
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        symbol.refresh_from_db()
        equity.refresh_from_db()
        self.assertEqual(symbol.ticker,"TELE")
        self.assertEqual(equity.company_name, 'UpdatedGoogle')

class SymbolTestWithFuture(Base):
    def setUp(self):
        super().setUp()
        
        # Set up required objects
        self.security_type = SecurityType.objects.create(value="FUT")
        self.venue = Venue.objects.create(value="CME")
        self.industry = Industry.objects.create(value="AGRICULTURE")
        self.currency = Currency.objects.create(value="USD")
        self.contract_units = ContractUnits.objects.create(value="Pounds")
        self.symbol = Symbol.objects.create(ticker="HEJ4", security_type=self.security_type)

        # URLs
        self.url = "/api/symbols/"

    def test_get_symbol_by_ticker(self):
        response = self.client.get(self.url, {'ticker': 'HEJ4'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['ticker'], 'HEJ4')

    def test_create_symbol_with_future(self):
        data = {
            'ticker': 'HEZ4',
            'security_type': self.security_type.value,
            'symbol_data': {
                            'product_code': "HE", 
                            'product_name': "Lean Hogs", 
                            'venue': self.venue.value, 
                            'currency': self.currency.value,
                            'contract_size': 40000, 
                            'contract_units':self.contract_units.value, 
                            'tick_size': 0.000025, 
                            'min_price_fluctuation':10, 
                            'continuous': False
                            }
            }
        
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Symbol.objects.count(), 2)
        self.assertEqual(Future.objects.count(), 1)
        self.assertEqual(Future.objects.last().product_code, 'HE')

    def test_delete_symbol_with_future(self):
        symbol = Symbol.objects.create(ticker="TTV", security_type=self.security_type)
        future = Future.objects.create(symbol=symbol, product_code="HE", product_name="Lean Hogs", venue=self.venue, 
                            currency=self.currency, contract_size=40000, contract_units=self.contract_units, 
                            tick_size=0.000025, min_price_fluctuation=10, continuous=False)

        url = f"{self.url}{symbol.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Symbol.objects.count(), 1)
        self.assertEqual(Future.objects.count(), 0)

    def test_update_symbol_with_future(self):
        symbol = Symbol.objects.create(ticker="TTV", security_type=self.security_type)
        future = Future.objects.create(symbol=symbol, product_code="HE", product_name="Lean Hogs", venue=self.venue, 
                            currency=self.currency, contract_size=40000, contract_units=self.contract_units, 
                            tick_size=0.000025, min_price_fluctuation=10, continuous=False)
        data = {
            'ticker': 'TELE',
            'security_type': self.security_type.value,
            'symbol_data': {
                            'product_code': "TTT", 
                            'product_name': "Lean Hogs", 
                            'venue': self.venue.value, 
                            'currency': self.currency.value,
                            'contract_size': 40000, 
                            'contract_units':self.contract_units.value, 
                            'tick_size': 0.000025, 
                            'min_price_fluctuation':10, 
                            'continuous': False
                            }
            }
        url = f"{self.url}{symbol.id}/"
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        symbol.refresh_from_db()
        future.refresh_from_db()
        self.assertEqual(symbol.ticker,"TELE")
        self.assertEqual(future.product_code, 'TTT')

class SymbolTestWithIndex(Base):
    def setUp(self):
        super().setUp()
        
        # Set up required objects
        self.security_type = SecurityType.objects.create(value="IND")
        self.venue = Venue.objects.create(value="NASDAQ")
        self.currency = Currency.objects.create(value="USD")
        self.asset_class = AssetClass.objects.create(value="EQUITY")
        self.symbol = Symbol.objects.create(ticker="DOJI", security_type=self.security_type)

        # URLs
        self.url = "/api/symbols/"

    def test_get_symbol_by_ticker(self):
        response = self.client.get(self.url, {'ticker': 'DOJI'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['ticker'], 'DOJI')

    def test_create_symbol_with_future(self):
        data = {
            'ticker': 'GSPC',
            'security_type': self.security_type.value,
            'symbol_data': {
                            'name': "S&P 500", 
                            'currency': self.currency.value,
                            'venue': self.venue.value, 
                            'asset_class': self.asset_class.value
                            }
            }
        
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Symbol.objects.count(), 2)
        self.assertEqual(Index.objects.count(), 1)
        self.assertEqual(Index.objects.last().name, 'S&P 500')

    def test_delete_symbol_with_index(self):
        symbol = Symbol.objects.create(ticker="TTV", security_type=self.security_type)
        index = Index.objects.create(symbol=symbol, name="S&P 500", currency=self.currency,venue=self.venue, asset_class=self.asset_class)

        url = f"{self.url}{symbol.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Symbol.objects.count(), 1)
        self.assertEqual(Index.objects.count(), 0)

    def test_update_symbol_with_index(self):
        symbol = Symbol.objects.create(ticker="TTV", security_type=self.security_type)
        index = Index.objects.create(symbol=symbol, name="S&P 500", currency=self.currency,venue=self.venue, asset_class=self.asset_class)
        data = {
            'ticker': 'XTXT',
            'security_type': self.security_type.value,
            'symbol_data': {
                            'name': "Russell 2000", 
                            'currency': self.currency.value,
                            'venue': self.venue.value, 
                            'asset_class': self.asset_class.value
                            }
            }
        url = f"{self.url}{symbol.id}/"
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        symbol.refresh_from_db()
        index.refresh_from_db()
        self.assertEqual(symbol.ticker,"XTXT")
        self.assertEqual(index.name, 'Russell 2000')

class EquityViewSetTest(Base):
    def setUp(self):
        super().setUp()

        # Set up required objects
        self.security_type = SecurityType.objects.create(value="STOCK")
        self.venue = Venue.objects.create(value="NASDAQ")
        self.industry = Industry.objects.create(value="Technology")
        self.currency = Currency.objects.create(value="USD")
        self.symbol = Symbol.objects.create(ticker="AAPL", security_type=self.security_type)
        self.equity = Equity.objects.create(symbol=self.symbol, 
                                            company_name="Google", 
                                            venue=self.venue, 
                                            currency=self.currency, 
                                            industry=self.industry,
                                            market_cap=10000000,
                                            shares_outstanding=90909090)
        # URLs
        self.url = "/api/equities/"

    def test_retrieve_equity(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['company_name'], 'Google')

    def test_create_equity_not_allowed(self):
        data = {'company_name': "UpdatedGoogle", 'venue': self.venue.value, 'currency': self.currency.value,'industry': self.industry.value,
                'market_cap': 2000000,'shares_outstanding': 9000000,"symbol":self.symbol.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 405)

    def test_update_equity_not_allowed(self):
        data = {'company_name': "UpdatedGoogle", 'venue': self.venue.value, 'currency': self.currency.value,'industry': self.industry.value,
                'market_cap': 2000000,'shares_outstanding': 9000000,"symbol":self.symbol.id}
        url = f"{self.url}/"
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, 405)

    def test_delete_equity_not_allowed(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 405)

class FutureViewSetTest(Base):
    def setUp(self):
        super().setUp()

        # Set up required objects
        self.security_type = SecurityType.objects.create(value="FUTURE")
        self.venue = Venue.objects.create(value="CME")
        self.contract_units = ContractUnits.objects.create(value="Pounds")
        self.currency = Currency.objects.create(value="USD")
        symbol = Symbol.objects.create(ticker="HEJ4", security_type=self.security_type)
        future = Future.objects.create(symbol=symbol, product_code="HE", product_name="Lean Hogs", venue=self.venue, 
                            currency=self.currency, contract_size=40000, contract_units=self.contract_units, 
                            tick_size=0.000025, min_price_fluctuation=10, continuous=False)

        # URLs
        self.url = "/api/futures/"

    def test_retrieve_future(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['product_code'], 'HE')

    def test_create_future_not_allowed(self):
        data = {'product_code': "tt"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 405)

    def test_update_future_not_allowed(self):
        data = {'product_code': "tt"}
        url = f"{self.url}/"
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, 405)

    def test_delete_future_not_allowed(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 405)

class IndexViewSetTest(Base):
    def setUp(self):
        super().setUp()

        # Set up required objects
        self.security_type = SecurityType.objects.create(value="INDEX")
        self.venue = Venue.objects.create(value="CME")
        self.contract_units = ContractUnits.objects.create(value="Pounds")
        self.currency = Currency.objects.create(value="USD")
        self.asset_class = AssetClass.objects.create(value="EQUITY")
        symbol = Symbol.objects.create(ticker="TTV", security_type=self.security_type)
        index = Index.objects.create(symbol=symbol, name="S&P 500", currency=self.currency,venue=self.venue, asset_class=self.asset_class)

        # URLs
        self.url = "/api/indexes/"

    def test_retrieve_index(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'S&P 500')

    def test_create_index_not_allowed(self):
        data = {'product_code': "tt"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 405)

    def test_update_index_not_allowed(self):
        data = {'product_code': "tt"}
        url = f"{self.url}/"
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, 405)

    def test_delete_index_not_allowed(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 405)