from rest_framework import serializers
from .models import Asset, Equity, Cryptocurrency, Future, Option
from rest_framework.exceptions import APIException
import logging

logger = logging.getLogger(__name__)

class AssetWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'symbol', 'security_type', 'created_at', 'updated_at']

class EquitySerializer(serializers.ModelSerializer):
    # asset_id = serializers.IntegerField(source='asset.id', read_only=True)  # Add this line
    asset_data = AssetWriteSerializer(write_only=True)

    class Meta:
        model = Equity
        fields = ['asset_data', 'company_name', 'exchange', 'currency', 'industry', 'market_cap', 'shares_outstanding', 'created_at', 'updated_at']

    def create(self, validated_data):
        try:
            asset_data = validated_data.pop('asset_data')
            asset = Asset.objects.create(**asset_data)
            equity = Equity.objects.create(asset=asset, **validated_data)
            return equity
        except Exception as e:
            # Log the exception for debugging
            logger.error(f"Error in perform_create: {str(e)}")
            # Raise an APIException with a custom message
            raise APIException("Failed to create equity. Please check your data.")

    def update(self, instance, validated_data):
        asset_data = validated_data.pop('asset_data', None)
        asset = instance.asset

        # Update the Asset instance
        if asset_data:
            for attr, value in asset_data.items():
                setattr(asset, attr, value)
            asset.save()

        # Update the Equity instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class FutureSerializer(serializers.ModelSerializer):
    asset_data = AssetWriteSerializer(write_only=True)

    class Meta:
        model = Future
        fields = ['asset_data','product_code','product_name', 'exchange','currency','contract_size','contract_units','tick_size','min_price_fluctuation', 'continuous','created_at','updated_at']

    def create(self, validated_data):
        asset_data = validated_data.pop('asset_data')
        asset = Asset.objects.create(**asset_data)
        future = Future.objects.create(asset=asset, **validated_data)
        return future

    def update(self, instance, validated_data):
        asset_data = validated_data.pop('asset_data', None)
        asset = instance.asset

        # Update the Asset instance
        if asset_data:
            for attr, value in asset_data.items():
                setattr(asset, attr, value)
            asset.save()

        # Update the Equity instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class CryptocurrencySerializer(serializers.ModelSerializer):
    asset_data = AssetWriteSerializer(write_only=True)

    class Meta:
        model = Cryptocurrency
        fields = ['asset_data', 'cryptocurrency_name', 'circulating_supply', 'market_cap', 'total_supply', 'max_supply', 'description', 'created_at', 'updated_at']

    def create(self, validated_data):
        asset_data = validated_data.pop('asset_data')
        asset = Asset.objects.create(**asset_data)
        cryptocurrency = Cryptocurrency.objects.create(asset=asset, **validated_data)
        return cryptocurrency

    def update(self, instance, validated_data):
        asset_data = validated_data.pop('asset_data', None)
        asset = instance.asset

        # Update the Asset instance
        if asset_data:
            for attr, value in asset_data.items():
                setattr(asset, attr, value)
            asset.save()

        # Update the Equity instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class OptionSerializer(serializers.ModelSerializer):
    asset_data = AssetWriteSerializer(write_only=True)

    class Meta:
        model = Option
        fields = ['asset_data', 'strike_price', 'expiration_date', 'option_type', 'contract_size','underlying_name','exchange','created_at','updated_at']

    def create(self, validated_data):
        asset_data = validated_data.pop('asset_data')
        asset = Asset.objects.create(**asset_data)
        option = Option.objects.create(asset=asset, **validated_data)
        return option

    def update(self, instance, validated_data):
        asset_data = validated_data.pop('asset_data', None)
        asset = instance.asset

        # Update the Asset instance
        if asset_data:
            for attr, value in asset_data.items():
                setattr(asset, attr, value)
            asset.save()

        # Update the Equity instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
    
class AssetReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'symbol', 'security_type', 'created_at', 'updated_at']

    def to_representation(self, instance):
        """Customize the serialization based on the asset type."""
        representation = super().to_representation(instance)

        if hasattr(instance, 'equity'):
            equity_data = EquitySerializer(instance.equity).data
            representation.update(equity_data)  # Merge equity data into the main representation
        # elif hasattr(instance, 'commodity'):
        #     commodity_data = CommoditySerializer(instance.commodity).data
        #     representation.update(commodity_data)  # Merge commodity data
        elif hasattr(instance, 'cryptocurrency'):
            cryptocurrency_data = CryptocurrencySerializer(instance.cryptocurrency).data
            representation.update(cryptocurrency_data)  # Merge cryptocurrency data
        elif hasattr(instance, 'future'):
            future_data = FutureSerializer(instance.future).data
            representation.update(future_data)  # Merge cryptocurrency data
        elif hasattr(instance, 'option'):
            option_data = OptionSerializer(instance.option).data
            representation.update(option_data)  # Merge cryptocurrency data
        
        return representation
    
