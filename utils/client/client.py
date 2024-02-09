import requests
from typing import List, Dict
from queue import Queue
import pandas as pd
from enum import Enum
from datetime import datetime, timedelta


class SecurityType(Enum):
    EQUITY = 'EQUITY'
    FUTURE = 'FUTURE'
    OPTION = 'OPTION'
    BENCHMARK = 'BENCHMARK'

class Exchange(Enum):   
    NASDAQ = 'NASDAQ'
    CME = 'CME'                   

class Currency(Enum):   
    USD='USD'
    CAD='CAD'              

class Indsutry(Enum):
    # Equities
    ENERGY='Energy'
    MATERIALS='Materials'
    INDUSTRIALS='Industrials'
    UTILITIES='Utilities'
    HEALTHCARE='Healthcare'
    FINANCIALS='Financials'
    CONSUMER='Consumer'
    TECHNOLOGY='Technology'
    COMMUNICATION='Communication'
    REAL_ESTATE='Real Estate'   
    
    # Commodities
    METALS='Metals' 
    AGRICULTURE='Agriculture'
    #ENERGY         

class ContractUnits(Enum):
    BARRELS='Barrels'
    BUSHELS='Bushels'
    POUNDS='Pounds'
    TROY_OUNCE='Troy Ounce'
    METRIC_TON='Metric Ton'
    SHORT_TON='Short Ton'

class DatabaseClient:
    def __init__(self, api_key:str, api_url:str ='http://127.0.0.1:8000'):
        self.api_url = api_url
        self.api_key = api_key

    # -- Symbols -- 
    def create_asset_class(self, name: str, description: str):
        """
        Creates a new asset class.

        Parameters:
        name (str): The name of the asset class.
        description (str): The description of the asset class.
        """
        url = f"{self.api_url}/api/asset_class/"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.api_key}"
        }
        data = {
            "name": name,
            "description": description
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 201:
            raise ValueError(f"Asset class creation failed: {response.text}")
        return response.json() 
    
    def get_asset_classes(self):
        """
        Retrieves all asset classes.
        """
        url = f"{self.api_url}/api/asset_class/"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {self.api_key}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise ValueError(f"Fetching asset classes failed: {response.text}")
        return response.json()
    
    def update_asset_class(self, asset_class_id: int, description: str):
        """
        Updates the description of an existing asset class.

        Parameters:
        asset_class_id (int): The ID of the asset class to update.
        description (str): The new description for the asset class.
        """
        url = f"{self.api_url}/api/asset_class/{asset_class_id}/"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {self.api_key}"
        }
        data = {
            "description": description
        }
        response = requests.patch(url, json=data, headers=headers)
        if response.status_code != 200:
            raise ValueError(f"Asset class update failed: {response.text}")
        return response.json()

    def create_currency(self, code: str, name: str, region: str):
        """
        Creates a new currency.

        Parameters:
        code (str): The currency code (e.g., USD).
        name (str): The name of the currency (e.g., US Dollar).
        region (str): The region or country where the currency is used.
        """
        url = f"{self.api_url}/api/currency/"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {self.api_key}"
        }
        data = {
            "code": code,
            "name": name,
            "region": region
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 201:
            raise ValueError(f"Currency creation failed: {response.text}")
        return response.json()

    def get_currencies(self):
        """
        Retrieves all currencies.
        """
        url = f"{self.api_url}/api/currency/"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {self.api_key}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise ValueError(f"Fetching currencies failed: {response.text}")
        return response.json()

    def update_currency(self, currency_id: int, **updates):
        """
        Updates information for an existing currency.

        Parameters:
        currency_id (int): The ID of the currency to update.
        **updates: Arbitrary number of keyword arguments representing the fields to update.
        """
        url = f"{self.api_url}/api/currency/{currency_id}/"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {self.api_key}"
        }
        data = updates
        response = requests.patch(url, json=data, headers=headers)
        if response.status_code != 200:
            raise ValueError(f"Currency update failed: {response.text}")
        return response.json()
    
    def create_benchmark(self, ticker: str, security_type: str, benchmark_name: str, asset_class: str, currency: str):
        """
        Creates a new benchmark.

        Parameters:
        ticker (str): The ticker symbol of the benchmark.
        security_type (str): The type of security, e.g., "BENCHMARK".
        benchmark_name (str): The name of the benchmark.
        asset_class (str): The asset class the benchmark belongs to.
        currency (str): The currency of the benchmark.
        """
        url = f"{self.api_url}/api/benchmark/"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {self.api_key}"
        }
        data = {
            "symbol_data": {
                "ticker": ticker,
                "security_type": security_type
            },
            "benchmark_name": benchmark_name,
            "asset_class": asset_class,
            "currency": currency
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 201:
            raise ValueError(f"Benchmark creation failed: {response.text}")
        return response.json()

    def update_benchmark(self, benchmark_id: int, **updates):
        """
        Updates information for an existing benchmark.

        Parameters:
        benchmark_id (int): The ID of the benchmark to update.
        **updates: Arbitrary number of keyword arguments representing the fields to update.
        """
        url = f"{self.api_url}/api/benchmark/{benchmark_id}/"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {self.api_key}"
        }
        data = updates
        response = requests.patch(url, json=data, headers=headers)
        if response.status_code != 200:
            raise ValueError(f"Benchmark update failed: {response.text}")
        return response.json()

    def get_benchmarks(self):
        """
        Retrieves all benchmarks.
        """
        url = f"{self.api_url}/api/benchmark/"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {self.api_key}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise ValueError(f"Fetching benchmarks failed: {response.text}")
        return response.json()
    
    def create_equity(self, **equity_data):
        """
        **equity_data = {
            "ticker": str,
            "security_type": SecurityType,  
            "company_name": str,
            "exchange": Exchange,       
            "currency": Currency,       
            "industry": Indsutry,  
            "market_cap": int,
            "shares_outstanding": int
        }
        
        """
        required_keys = {
            "ticker": str,
            "security_type": SecurityType,  
            "company_name": str,
            "exchange": Exchange,       
            "currency": Currency,       
            "industry": Indsutry,  
            "market_cap": int,
            "shares_outstanding": int
        }

        # Check for missing required keys and type validation
        for key, expected_type in required_keys.items():
            if key not in equity_data:
                raise ValueError(f"{key} is required.")
            if not isinstance(equity_data[key], expected_type):
                raise TypeError(f"Incorrect type for {key}. Expected {expected_type.__name__}, got {type(equity_data[key]).__name__}")

        # Prepare the data payload
        data = {
            "symbol_data": {
                "ticker": equity_data["symbol"],
                "security_type": equity_data["security_type"].value
            },
            "company_name": equity_data["company_name"],
            "exchange": equity_data["exchange"].value,
            "currency": equity_data["currency"].value,
            "industry": equity_data["industry"].value,
            "market_cap": equity_data["market_cap"],
            "shares_outstanding": equity_data["shares_outstanding"]
        }
        url = f"{self.api_url}/api/equities/"
        headers = {'Authorization': f'Token {self.api_key}'}
        response = requests.post(url, json=data, headers=headers)

        if response.status_code != 201:
            raise ValueError(f"Asset creation failed: {response.text}")
        return response.json()

    def create_future(self, **future_data):
        """    
        future_data = {
            "ticker": str,
            "security_type": SecurityType,  
            "product_code":str,
            "product_name": str,
            "exchange": Exchange,       
            "currency": Currency,       
            "contract_size":int,    
            "contract_units":ContractUnits,
            "tick_size":float,   
            "min_price_fluctuation":float,    
            "continuous":bool
        }
        """
        
        required_keys = {
            "ticker": str,
            "security_type": SecurityType,  
            "product_code":str,
            "product_name": str,
            "exchange": Exchange,       
            "currency": Currency,       
            "contract_size":int,    
            "contract_units":ContractUnits,
            "tick_size":float,   
            "min_price_fluctuation":float,    
            "continuous":bool
        }

        # Check for missing required keys and type validation
        for key, expected_type in required_keys.items():
            if key not in future_data:
                raise ValueError(f"{key} is required.")
            if not isinstance(future_data[key], expected_type):
                raise TypeError(f"Incorrect type for {key}. Expected {expected_type.__name__}, got {type(future_data[key]).__name__}")
        
        data = {
                'symbol_data': {
                    'ticker': future_data['ticker'],
                    'security_type': future_data['security_type'].value
                    },

                'product_code':future_data['product_code'],
                'product_name':future_data['product_name'], 
                'exchange':future_data['exchange'].value,
                'currency':future_data['currency'].value,
                'contract_size':future_data['contract_size'],
                'contract_units':future_data['contract_units'].value,
                'tick_size':future_data['tick_size'],
                'min_price_fluctuation':future_data['min_price_fluctuation'],
                'comtinuous':future_data['continuous']
                }
        
        url = f"{self.api_url}/api/futures/"
        headers = {'Authorization': f'Token {self.api_key}'}
        response = requests.post(url, json=data, headers=headers)

        if response.status_code != 201:
            raise ValueError(f"Asset creation failed: {response.text}")
        return response.json()
    
    def get_asset_by_symbol(self, ticker: str):
        url = f"{self.api_url}/api/symbols/"
        params = {'ticker': ticker}
        headers = {'Authorization': f'Token {self.api_key}'}
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            raise ValueError(f"Failed to retrieve asset by symbol: {response.text}")
    
    def get_assets(self):
        url = f"{self.api_url}/api/symbols/"
        headers = {'Authorization': f'Token {self.api_key}'}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise ValueError(f"Failed to retrieve assets: {response.text}")
        return response.json()
    
    # -- Bar Data -- 
    def create_bar_data(self, bar_data: Dict):
        url = f"{self.api_url}/api/bardata/"
        headers = {'Authorization': f'Token {self.api_key}'}
        response = requests.post(url, json=bar_data, headers=headers)

        if response.status_code != 201:
            raise ValueError(f"Bar data creation failed: {response.text}")
        return response.json()
    
    def create_bulk_price_data(self, bulk_data: List[Dict]):
        batch_size = 400
        total_batches = len(bulk_data) // batch_size + (1 if len(bulk_data) % batch_size > 0 else 0)
        all_responses = []

        for batch_number in range(total_batches):
            # Extract the current batch
            start_index = batch_number * batch_size
            end_index = start_index + batch_size
            current_batch = bulk_data[start_index:end_index]

            # Send the batch request
            url = f"{self.api_url}/api/bardata/bulk_create/"
            headers = {'Authorization': f'Token {self.api_key}'}
            response = requests.post(url, json=current_batch, headers=headers)

            if response.status_code != 201:
                raise ValueError(f"Bulk bar data creation failed for batch {batch_number + 1}: {response.text}")
            
            all_responses.append(response.json())

        # Aggregate all responses
        aggregated_response = {
            'total_batches': total_batches,
            'batch_responses': all_responses
        }
        return aggregated_response
    
    def get_bar_data(self, tickers: List[str], start_date: str = None, end_date: str = None):
        if start_date is None or end_date is None:
            raise ValueError("Start date and end date must be provided for batching")

        batch_size = 50
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        current_start = start
        all_data = []

        while current_start < end:
            current_end = min(current_start + timedelta(days=batch_size), end)
            # Adjust the end date to avoid including it in the next batch
            adjusted_end_date = (current_end - timedelta(days=1)).strftime('%Y-%m-%d') if current_end != end else current_end.strftime('%Y-%m-%d')

            batch_data = self._fetch_batch_data(tickers, current_start.strftime('%Y-%m-%d'), adjusted_end_date)
            all_data.extend(batch_data)
            # Set the start of the next batch to the day after the current batch's end
            current_start = current_end
        return all_data 

    def _fetch_batch_data(self, tickers, start_date, end_date):
        url = f"{self.api_url}/api/bardata/"
        params = {
            'tickers': ','.join(tickers),
            'start_date': start_date,
            'end_date': end_date
        }
        headers = {'Authorization': f'Token {self.api_key}'}
        response = requests.get(url, params=params, headers=headers)

        if response.status_code != 200:
            raise ValueError(f"Failed to retrieve bar data for batch {start_date} to {end_date}: {response.text}")

        return response.json()
    
    # -- Backtest Data -- 
    def create_backtest(self, data):
        """
        Create a new backtest.
        :param data: Dictionary containing backtest data.
        :return: Response from the API.
        """
        url = f"{self.api_url}/api/backtest/"
        headers = {'Authorization': f'Token {self.api_key}'}
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code != 201:
            raise ValueError(f"Backtest creation failed: {response.text}")
        return response.json()

    def get_backtests(self):
        """
        Retrieve all backtests.
        :return: List of backtests.
        """
        url = f"{self.api_url}/api/backtest/"
        headers = {'Authorization': f'Token {self.api_key}'}
        response = requests.get(url, headers = {'Authorization': f'Token {self.api_key}'})

        if response.status_code != 200:
            raise ValueError(f"Failed to retrieve backtests: {response.text}")
        return response.json()

    def get_specific_backtest(self, backtest_id):
        """
        Retrieve a specific backtest by ID.
        :param backtest_id: ID of the backtest to retrieve.
        :return: Backtest data.
        """
        url = f"{self.api_url}/api/backtest/{backtest_id}/"
        headers = {'Authorization': f'Token {self.api_key}'}
        response = requests.get(url, headers)
        
        if response.status_code != 200:
            raise ValueError(f"Failed to retrieve backtest: {response.text}")
        return response.json()

   