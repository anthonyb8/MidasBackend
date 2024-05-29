import logging
from django.db import transaction
from django.core.exceptions import ValidationError

from symbols.models import Symbol
from market_data.models import BarData
from market_data.serializers import BarDataSerializer
from regression_analysis.models import RegressionAnalysis
from regression_analysis.serializers import RegressionAnalysisSerializer
from .models import Backtest, StaticStats, TimeseriesStats, Trade, Signal, TradeInstruction

logger = logging.getLogger()


def create_backtest(validated_data):
    try:
        with transaction.atomic():
            logger.info("Starting backtest creation process.")

            # Extract nested data
            parameters = validated_data.pop('parameters', {})
            static_stats_data = validated_data.pop('static_stats', [])
            regression_data = validated_data.pop('regression_stats', [])
            timeseries_stats_data = validated_data.pop('timeseries_stats', [])
            trades_data = validated_data.pop('trades', [])
            signals_data = validated_data.pop('signals', [])

            # Create the Backtest instance
            backtest = Backtest.objects.create(**parameters)
            logger.info(f"Backtest instance created with ID: {backtest.id}")

            # Nested object creation for SummaryStats
            for stat_data in static_stats_data:
                StaticStats.objects.create(backtest=backtest, **stat_data)
            logger.info("Static stats created.")
            
            # Nested object creation for RegressionAnalysis
            for stat_data in regression_data:
                RegressionAnalysis.objects.create(backtest=backtest, **stat_data)
            logger.info("Regression stats created.")

            # Nested object creation for TimeseriesStats
            for stat_data in timeseries_stats_data:
                TimeseriesStats.objects.create(backtest=backtest, **stat_data)
            logger.info("Timeseries stats created.")

            # Nested object creation for Trades
            for trade_data in trades_data:
                Trade.objects.create(backtest=backtest, **trade_data)
            logger.info("Trades created.")

            # Nested object creation for Signals and their TradeInstructions
            for signal_data in signals_data:
                trade_instructions_data = signal_data.pop('trade_instructions', [])
                signal_instance = Signal.objects.create(backtest=backtest, **signal_data)
                for ti_data in trade_instructions_data:
                    TradeInstruction.objects.create(signal=signal_instance, **ti_data)
            logger.info("Signals and trade instructions created.")

            return backtest

    except ValidationError as e:
        logger.error(f"Validation error during backtest creation: {e}")
        # Re-raise the error if you want to notify the caller
        raise e
    except Exception as e:
        logger.exception(f"Unexpected error during backtest creation: {e}")
        # Re-raise or handle the error as appropriate
        raise e
    
def fetch_price_data(backtest_instance):
    try:
        logger.info("Starting to fetch price data for tickers: %s", backtest_instance.tickers)
        ticker_list = backtest_instance.tickers
        
        # Fetching Symbol objects for each ticker
        symbol_objs = Symbol.objects.filter(ticker__in=ticker_list)
        if not symbol_objs.exists():
            logger.error(f"No Symbol objects found for tickers: {ticker_list}")
            return []
        
        # Filter BarData based on Symbol objects and the date range
        price_data = BarData.objects.filter(
            symbol__in=symbol_objs,
            timestamp__gte=backtest_instance.test_start,
            timestamp__lte=backtest_instance.test_end
        ).order_by('timestamp')
        
        logger.info(f"Fetched {price_data.count()} price data records for backtest {backtest_instance.id}.")
        return price_data
    except Exception as e:
        logger.exception(f"Failed to fetch price data for backtest {backtest_instance.id}: {str(e)}")
        return []
    
def get_price_data(backtest_instance):
    try:
        price_data = fetch_price_data(backtest_instance)
        serializer = BarDataSerializer(price_data, many=True)
        return serializer.data
    except Exception as e:
        logger.exception(f"Error serializing price data for backtest {backtest_instance.id}: {str(e)}")
        return []

def get_regression_data(backtest_instance):
    try:
        regression_data = RegressionAnalysis.objects.get(backtest=backtest_instance)
        serializer = RegressionAnalysisSerializer(regression_data)
        return serializer.data
    except RegressionAnalysis.DoesNotExist:
        logger.warning(f"No regression data found for backtest {backtest_instance.id}")
        return []
    except Exception as e:
        logger.exception(f"Error serializing regression data for backtest {backtest_instance.id}: {str(e)}")
        return []

