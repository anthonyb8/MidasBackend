import logging
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from symbols.models import Symbol
from market_data.models import BarData
from market_data.serializers import BarDataSerializer
from .services import create_live_session, get_price_data
from .models import LiveSession, AccountSummary, Trade, Signal, TradeInstruction

logger = logging.getLogger()

class AccountSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSummary
        fields = ["currency", "start_timestamp", "start_buying_power", "start_excess_liquidity", "start_full_available_funds", "start_full_init_margin_req", "start_full_maint_margin_req", 
                  "start_futures_pnl", "start_net_liquidation", "start_total_cash_balance", "start_unrealized_pnl", "end_timestamp", "end_buying_power", "end_excess_liquidity", "end_full_available_funds",
                  "end_full_init_margin_req", "end_full_maint_margin_req", "end_futures_pnl", "end_net_liquidation", "end_total_cash_balance", "end_unrealized_pnl"]

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ['timestamp', 'ticker', 'quantity', 'price', 'cost', 'action', 'fees']

class TradeInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeInstruction
        fields = ['ticker', 'action', 'trade_id', 'leg_id', 'weight']

class SignalSerializer(serializers.ModelSerializer):
    trade_instructions = TradeInstructionSerializer(many=True)

    class Meta:
        model = Signal
        fields = ['timestamp', 'trade_instructions']
    
    def create(self, validated_data):
        try:
            with transaction.atomic():
                trade_instructions_data = validated_data.pop('trade_instructions', [])
                logger.info("Creating Signal object.")
                signal = Signal.objects.create(**validated_data)

                for ti_data in trade_instructions_data:
                    logger.info(f"Creating TradeInstruction object for signal {signal.id}.")
                    TradeInstruction.objects.create(signal=signal, **ti_data)

                logger.info(f"Successfully created Signal and TradeInstructions for signal {signal.id}.")
                return signal
        except Exception as e:
            logger.error(f"Error creating Signal and TradeInstructions: {str(e)}", exc_info=True)
            raise

class LiveSessionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveSession
        fields = ['id', 'strategy_name', 'tickers', 'benchmark', 'data_type', 'train_start', 'train_end', 'test_start', 'test_end', 'capital', 'created_at']

class LiveSessionSerializer(serializers.ModelSerializer):
    parameters = LiveSessionListSerializer(write_only=True)
    account_data = AccountSummarySerializer(many=True)
    trades = TradeSerializer(many=True)
    signals = SignalSerializer(many=True)
    price_data = BarDataSerializer(read_only=True)

    class Meta:
        model = LiveSession
        fields = ['id', 'parameters', 'account_data', 'trades', 'signals', 'price_data']
        
    def validate(self, data):
        logger.info(f"Validating data : {data}")
        try:
            validated_data = super().validate(data)
            logger.info(f"Validating successful.")
            return validated_data
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise e
    
    # POST
    def create(self, validated_data):
        logger.info("Creating a new LiveSession instance with data: %s", validated_data)
        try:
            live_session_instance = create_live_session(validated_data)
            logger.info(f"Successfully created LiveSession instance with ID: {live_session_instance.id}")
            return live_session_instance
        except Exception as e:
            logger.exception(f"Failed to create a new LiveSession instance: {str(e)}")
            raise serializers.ValidationError("Failed to create a new LiveSession instance")
        
    # PUT / PATCH
    def update(self, instance, validated_data):
        logger.info(f"Updating for LiveSession instance with ID: {instance.id}")
        try:
            parameters = validated_data.pop('parameters', {}) # can only update the parameters
            # Proceed with the default update process
            instance = super().update(instance, parameters)
            logger.info(f"Successfully updated LiveSession instance with ID: {instance.id}")
            return instance
        except Exception as e:
            logger.exception(f"Unexpected error during update of LiveSession instance with ID: {instance.id}: {e}")
            raise serializers.ValidationError(f"Update failed for unexpected reasons: {e}")

    # GET
    def to_representation(self, instance):
        logger.info(f"Retrieving a LiveSession instance with ID: {instance.id}")
        try:
            data = super().to_representation(instance)
            data['parameters']  = {
                "strategy_name": instance.strategy_name,
                "tickers": instance.tickers,
                "benchmark": instance.benchmark,
                "data_type": instance.data_type,
                "train_start": instance.train_start,
                "train_end": instance.train_end,
                "test_start": instance.test_start,
                "test_end": instance.test_end,
                "capital": instance.capital,
                "created_at": instance.created_at #.isoformat(),
            }
            data['price_data'] = get_price_data(instance)
            logger.info(f"Successfully retrieved LiveSession instance with ID: {instance.id}")
            return data
        except Exception as e:
            logger.exception(f"Error during representation of LiveSession {instance.id}: {str(e)}")
            return {"error": "An error occurred while processing the request."}  



