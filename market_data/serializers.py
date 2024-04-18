from rest_framework import serializers
from .models import BarData, QuoteData
from symbols.models import Symbol
import logging

logger = logging.getLogger(__name__)

class BarDataSerializer(serializers.ModelSerializer):
    symbol = serializers.SlugRelatedField(
        queryset=Symbol.objects.all(),
        slug_field='ticker', 
        write_only=False 
    )

    class Meta:
        model = BarData
        fields = ['id', 'symbol', 'timestamp', 'open', 'close', 'high', 'low', 'volume']

    def to_representation(self, instance):
        logger.info(f"Serializing BarData instance with ID: {instance.id}")
        try:
            ret = super().to_representation(instance)
            ret['symbol'] = instance.symbol.ticker
            logger.info(f"Successfully serialized BarData instance with ID: {instance.id}")
            return ret
        except Exception as e:
            logger.error(f"Error during serialization of BarData instance with ID: {instance.id}: {e}")
            return {}  # Or handle the error as appropriate

    def create(self, validated_data):
        logger.info(f"Attempting to create BarData with data: {validated_data}")
        try:
            bar_data = super().create(validated_data)
            logger.info(f"Successfully created BarData with ID: {bar_data.id}")
            return bar_data
        except Exception as e:
            logger.error(f"Failed to create BarData: {e}")
            raise serializers.ValidationError(f"Failed to create BarData: {e}")

    def update(self, instance, validated_data):
        logger.info(f"Attempting to update BarData with ID: {instance.id}")
        try:
            bar_data = super().update(instance, validated_data)
            logger.info(f"Successfully updated BarData with ID: {bar_data.id}")
            return bar_data
        except Exception as e:
            logger.error(f"Failed to update BarData with ID: {instance.id}: {e}")
            raise serializers.ValidationError(f"Failed to update BarData: {e}")

class QuoteDataSerializer(serializers.ModelSerializer):
    symbol = serializers.SlugRelatedField(
        queryset=Symbol.objects.all(),
        slug_field='ticker', 
        write_only=False  # Now allowing both read and write
    )
    class Meta:
        model = QuoteData
        fields = ['id', 'symbol', 'timestamp', 'ask', 'ask_size', 'bid', 'bid_size']

    def to_representation(self, instance):
        logger.info(f"Serializing QuoteData instance with ID: {instance.id}")
        try:
            ret = super().to_representation(instance)
            ret['symbol'] = instance.symbol.ticker
            logger.info(f"Successfully serialized QuoteData instance with ID: {instance.id}")
            return ret
        except Exception as e:
            logger.error(f"Error during serialization of QuoteData instance with ID: {instance.id}: {e}")
            return {}  # Or handle the error as appropriate

    def create(self, validated_data):
        logger.info(f"Attempting to create QuoteData with data: {validated_data}")
        try:
            quote_data = super().create(validated_data)
            logger.info(f"Successfully created QuoteData with ID: {quote_data.id}")
            return quote_data
        except Exception as e:
            logger.error(f"Failed to create QuoteData: {e}")
            raise serializers.ValidationError(f"Failed to create QuoteData: {e}")

    def update(self, instance, validated_data):
        logger.info(f"Attempting to update QuoteData with ID: {instance.id}")
        try:
            quote_data = super().update(instance, validated_data)
            logger.info(f"Successfully updated QuoteData with ID: {quote_data.id}")
            return quote_data
        except Exception as e:
            logger.error(f"Failed to update QuoteData with ID: {instance.id}: {e}")
            raise serializers.ValidationError(f"Failed to update QuoteData: {e}")
