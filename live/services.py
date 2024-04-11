import logging
from django.db import transaction
from django.core.exceptions import ValidationError

from symbols.models import Symbol
from market_data.models import BarData
from market_data.serializers import BarDataSerializer
from .models import LiveSession, AccountSummary, Trade, Signal, TradeInstruction

logger = logging.getLogger()


def create_live_session(validated_data):
    try:
        with transaction.atomic():
            logger.info("Starting live_session creation process.")

            # Extract nested data
            parameters = validated_data.pop('parameters', {})
            account_data = validated_data.pop('account_data', [])
            trades_data = validated_data.pop('trades', [])
            signals_data = validated_data.pop('signals', [])

            # Create the live_session instance
            live_session = LiveSession.objects.create(**parameters)
            logger.info(f"live_session instance created with ID: {live_session.id}")

            # Nested object creation for SummaryStats
            for stat_data in account_data:
                AccountSummary.objects.create(live_session=live_session, **stat_data)
            logger.info("Account summary created.")

            # Nested object creation for Trades
            for trade_data in trades_data:
                Trade.objects.create(live_session=live_session, **trade_data)
            logger.info("Trades created.")

            # Nested object creation for Signals and their TradeInstructions
            for signal_data in signals_data:
                trade_instructions_data = signal_data.pop('trade_instructions', [])
                signal_instance = Signal.objects.create(live_session=live_session, **signal_data)
                for ti_data in trade_instructions_data:
                    TradeInstruction.objects.create(signal=signal_instance, **ti_data)
            logger.info("Signals and trade instructions created.")

            return live_session

    except ValidationError as e:
        logger.error(f"Validation error during live_session creation: {e}")
        # Re-raise the error if you want to notify the caller
        raise e
    except Exception as e:
        logger.exception(f"Unexpected error during live_session creation: {e}")
        # Re-raise or handle the error as appropriate
        raise e
    
def fetch_price_data(live_session_instance):
    try:
        logger.info("Starting to fetch price data for tickers: %s", live_session_instance.tickers)
        ticker_list = live_session_instance.tickers
        
        # Fetching Symbol objects for each ticker
        symbol_objs = Symbol.objects.filter(ticker__in=ticker_list)
        if not symbol_objs.exists():
            logger.error(f"No Symbol objects found for tickers: {ticker_list}")
            return []
        
        # Filter BarData based on Symbol objects and the date range
        price_data = BarData.objects.filter(
            symbol__in=symbol_objs,
            timestamp__gte=live_session_instance.test_start,
            timestamp__lte=live_session_instance.test_end
        ).order_by('timestamp')
        
        logger.info(f"Fetched {price_data.count()} price data records for live_session {live_session_instance.id}.")
        return price_data
    except Exception as e:
        logger.exception(f"Failed to fetch price data for live_session {live_session_instance.id}: {str(e)}")
        return []
    
def get_price_data(live_session_instance):
    try:
        price_data = fetch_price_data(live_session_instance)
        serializer = BarDataSerializer(price_data, many=True)
        return serializer.data
    except Exception as e:
        logger.exception(f"Error serializing price data for live_session {live_session_instance.id}: {str(e)}")
        return []
