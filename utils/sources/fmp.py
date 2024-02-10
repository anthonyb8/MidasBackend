import json
import requests
import pandas as pd
from enum import Enum
from decouple import config
from ..client import DatabaseClient, SecurityType, Exchange,Indsutry, Currency, ContractUnits, AssetClass
# import databento as db
# from decouple import config
# import datetime
# from urllib.request import urlopen
# import certifi
# import json
# from urllib.request import urlopen, urlencode


DATABASE_KEY = config('LOCAL_API_KEY')
DATABASE_URL = config('LOCAL_URL')

    
class FMPClient:
    def __init__(self, api_key:str, api_url:str ='https://financialmodelingprep.com/api/v3/'):
        self.api_url = api_url
        self.api_key = api_key

    def get_historical_data(self, symbol, start_date, end_date, serietype='line'):
        """
        Fetches historical price data for a given stock symbol using requests library.

        Parameters:
        symbol (str): The stock symbol to fetch data for.
        start_date (str): Start date for the data in YYYY-MM-DD format.
        end_date (str): End date for the data in YYYY-MM-DD format.
        serietype (str): Type of data series ('line' by default).

        Returns:
        dict: A dictionary containing the historical price data.
        """
        url = f"{self.api_url}historical-price-full/{symbol}"
        params = {
            'apikey': self.api_key,
            'from': start_date,
            'to': end_date,
            'serietype': serietype
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Failed to fetch historical data: {response.text}")
    
    def get_available_indexes(self):
        """
        Fetches available indexes from the FinancialModelingPrep API.
            > https://financialmodelingprep.com/api/v3/symbol/available-indexes?apikey=8415942f9c72bf0c64ff9efb2a028add

        Returns:
        dict: A dictionary or list containing the available indexes.
        """
        # The API key is included directly in the URL, so you don't need to specify it again in the params.
        url = f"{self.api_url}symbol/available-indexes?apikey={self.api_key}"
        
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Failed to fetch available indexes: {response.text}")

if __name__ == "__main__":
    # Initialize the database client
    database = DatabaseClient(DATABASE_KEY,DATABASE_URL)


    # -- Create Currency --
    # USD = {
    #     'code':'CAD',
    #     'name':'Canadian Dollar',
    #     'region':'Canada',
    #     }
    # database.create_currency(**USD)

    # -- Create Asset Class --
    # EQUITY = {
    #         'name':'FIXED INCOME', 
    #         'description':'General fixed income type.'
    #        }
    # database.create_asset_class(**EQUITY)

    # -- Create Index --
    # GSPC = {
    #     'ticker':'^GSPC',
    #     'name':'S&P 500',
    #     'currency':Currency.USD,
    #     'security_type':SecurityType.INDEX,
    #     'asset_class': AssetClass.EQUITY
    #     }

    # database.create_index(**GSPC)

    # -- Create BarData -- 
    # data = {
    #     'symbol': "^GSPC",        
    #     "timestamp": "2024-01-01",  # Assuming timestamp is a string; adjust the type as needed
    #     "open": 100.0,
    #     "close": 100.0,
    #     "high": 100.0,
    #     "low": 100.0,
    #     "volume": 10000,  # Adjust types based on your specific requirements
    #     }
    # response = database.create_bar_data(**data)
    
    # -- Get BarData -- 
    tickers = ['^GSPC']
    start_date = "2024-01-01"
    end_date="2024-01-19"
    response = database.get_bar_data(tickers, start_date, end_date)
    print(response)


    # client = FMPClient(config('FMP_PRIMARY'))
    # data = client.get_available_indexes()        
    # print(data)

    # start_date = "2024-01-01"
    # end_date="2024-01-19"

    # # # -- Get Databento Continuous Future Data by Open Interest --
    # symbols = 'AAPL'
    # data = fmp_client.get_historical_data(symbols,start_date, end_date)    

    # # Check and create assets if they don't exist
    # for symbol in symbols:
    #     if not database.get_asset_by_symbol(symbol):
    #         raise Exception(f"{symbol} not present in database.")

    # Databento client
    # client = DatabentoClient(symbols, schema, dataset, stype, start_date, end_date)
    # data = client.get_data()

    # # Database client
    # response = database.create_bulk_price_data(data)
    # print(response)
