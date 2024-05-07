import logging
from django.db import transaction
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import APIException
from .models import Symbol, Equity, Cryptocurrency, Future, Option, AssetClass, Currency, Index, SecurityType, Venue, Industry, ContractUnits

logger = logging.getLogger(__name__)

# AssetDetails
class AssetClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetClass
        fields = ['id', 'value']

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'value']

class SecurityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityType
        fields = ['id', 'value']

class ContractUnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractUnits
        fields = ['id', 'value']

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'value']

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id', 'value']

# Assets
class SymbolSerializer(serializers.ModelSerializer):
    security_type = serializers.SlugRelatedField(slug_field="value", queryset=SecurityType.objects.all())
    symbol_data = serializers.DictField(required=False, write_only=True) 
    class Meta:
        model = Symbol
        fields = ['id', 'ticker', 'security_type', 'symbol_data']

    def create(self, validated_data):
        symbol_data = validated_data.pop('symbol_data', None)
        with transaction.atomic():
            symbol = Symbol.objects.create(**validated_data)
            if symbol.security_type.value == "STK":
                if symbol_data:
                    symbol_data['symbol'] = symbol.pk  # Pass symbol instance to equity_data
                    equity_serializer = EquitySerializer(data=symbol_data)
                    if equity_serializer.is_valid():
                        equity_serializer.save()
                    else:
                        raise serializers.ValidationError(equity_serializer.errors)
            elif symbol.security_type.value == "FUT":
                if symbol_data:
                    symbol_data['symbol'] = symbol.pk  # Pass symbol instance to equity_data
                    future_serializer = FutureSerializer(data=symbol_data)
                    if future_serializer.is_valid():
                        future_serializer.save()
                    else:
                        raise serializers.ValidationError(future_serializer.errors)
            elif symbol.security_type.value == "OPT":
                if symbol_data:
                    symbol_data['symbol'] = symbol.pk  # Pass symbol instance to equity_data
                    option_serializer = OptionSerializer(data=symbol_data)
                    if option_serializer.is_valid():
                        option_serializer.save()
                    else:
                        raise serializers.ValidationError(option_serializer.errors)
            elif symbol.security_type.value == "CRYPTO":
                if symbol_data:
                    symbol_data['symbol'] = symbol.pk  # Pass symbol instance to equity_data
                    cryptocurrency_serializer = CryptocurrencySerializer(data=symbol_data)
                    if cryptocurrency_serializer.is_valid():
                        cryptocurrency_serializer.save()
                    else:
                        raise serializers.ValidationError(cryptocurrency_serializer.errors)
            elif symbol.security_type.value == "IND":
                if symbol_data:
                    symbol_data['symbol'] = symbol.pk  # Pass symbol instance to equity_data
                    index_serializer = IndexSerializer(data=symbol_data)
                    if index_serializer.is_valid():
                        index_serializer.save()
                    else:
                        raise serializers.ValidationError(index_serializer.errors)
            else:
                raise serializers.ValidationError(detail=f"Model does not exist for given security_type.")

        return symbol
    
    def update(self, instance, validated_data):
        symbol_data = validated_data.pop('symbol_data', None)
        with transaction.atomic():
            # Update the symbol instance
            instance.ticker = validated_data.get('ticker', instance.ticker)
            instance.security_type = validated_data.get('security_type', instance.security_type)
            instance.save()

            if instance.security_type.value == "STK":
                # Delegate update or creation of related equity
                if symbol_data:
                    equity = getattr(instance, 'equity', None)
                    if equity:
                        # Pass the existing instance for updating
                        equity_serializer = EquitySerializer(equity, data=symbol_data, partial=True)
                    else:
                        # Pass new data for creation
                        symbol_data['symbol'] = instance
                        equity_serializer = EquitySerializer(data=symbol_data)

                    if equity_serializer.is_valid():
                        equity_serializer.save()
                    else:
                        raise serializers.ValidationError(equity_serializer.errors)
            elif instance.security_type.value == "FUT":
                # Delegate update or creation of related equity
                if symbol_data:
                    future = getattr(instance, 'future', None)
                    if future:
                        # Pass the existing instance for updating
                        future_serializer = FutureSerializer(future, data=symbol_data, partial=True)
                    else:
                        # Pass new data for creation
                        symbol_data['symbol'] = instance
                        future_serializer = FutureSerializer(data=symbol_data)

                    if future_serializer.is_valid():
                        future_serializer.save()
                    else:
                        raise serializers.ValidationError(future_serializer.errors)
            elif instance.security_type.value == "OPT":
                # Delegate update or creation of related equity
                if symbol_data:
                    option = getattr(instance, 'option', None)
                    if option:
                        # Pass the existing instance for updating
                        option_serializer = OptionSerializer(option, data=symbol_data, partial=True)
                    else:
                        # Pass new data for creation
                        symbol_data['symbol'] = instance
                        option_serializer = OptionSerializer(data=symbol_data)

                    if option_serializer.is_valid():
                        option_serializer.save()
                    else:
                        raise serializers.ValidationError(option_serializer.errors)
            elif instance.security_type.value == "CRYPTO":
                # Delegate update or creation of related equity
                if symbol_data:
                    cryptocurrency = getattr(instance, 'cryptocurrency', None)
                    if cryptocurrency:
                        # Pass the existing instance for updating
                        cryptocurrency_serializer = CryptocurrencySerializer(cryptocurrency, data=symbol_data, partial=True)
                    else:
                        # Pass new data for creation
                        symbol_data['symbol'] = instance
                        cryptocurrency_serializer = CryptocurrencySerializer(data=symbol_data)

                    if cryptocurrency_serializer.is_valid():
                        cryptocurrency_serializer.save()
                    else:
                        raise serializers.ValidationError(cryptocurrency_serializer.errors)
            elif instance.security_type.value == "IND":
                # Delegate update or creation of related equity
                if symbol_data:
                    index = getattr(instance, 'index', None)
                    if index:
                        # Pass the existing instance for updating
                        index_serializer = IndexSerializer(index, data=symbol_data, partial=True)
                    else:
                        # Pass new data for creation
                        symbol_data['symbol'] = instance
                        index_serializer = IndexSerializer(data=symbol_data)

                    if index_serializer.is_valid():
                        index_serializer.save()
                    else:
                        raise serializers.ValidationError(index_serializer.errors)
            else:
                raise serializers.ValidationError(detail=f"Model does not exist for given security_type.")
        return instance

class EquitySerializer(serializers.ModelSerializer):
    venue = serializers.SlugRelatedField(slug_field="value", queryset=Venue.objects.all(), required=False)
    currency = serializers.SlugRelatedField(slug_field="value", queryset=Currency.objects.all(), required=False)
    industry = serializers.SlugRelatedField(slug_field="value", queryset=Industry.objects.all(), required=False)
    symbol = serializers.PrimaryKeyRelatedField(queryset=Symbol.objects.all())
    # symbol = serializers.SlugRelatedField(slug_field="ticker", queryset=Symbol.objects.all(), required=False)

    class Meta:
        model = Equity
        fields = ['company_name', 'venue', 'currency', 'industry', 'market_cap', 'shares_outstanding', 'symbol']

    def create(self, validated_data):
        symbol = validated_data.get('symbol', None)
        equity = Equity.objects.create(**validated_data)
        return equity

    def update(self, instance, validated_data):
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.venue = validated_data.get('venue', instance.venue)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.industry = validated_data.get('industry', instance.industry)
        instance.market_cap = validated_data.get('market_cap', instance.market_cap)
        instance.shares_outstanding = validated_data.get('shares_outstanding', instance.shares_outstanding)
        instance.save()
        return instance
    
class FutureSerializer(serializers.ModelSerializer):
    venue = serializers.SlugRelatedField(slug_field="value", queryset=Venue.objects.all(), required=False)
    currency = serializers.SlugRelatedField(slug_field="value", queryset=Currency.objects.all(), required=False)
    industry = serializers.SlugRelatedField(slug_field="value", queryset=Industry.objects.all(), required=False)
    contract_units = serializers.SlugRelatedField(slug_field="value", queryset=ContractUnits.objects.all(), required=False)
    symbol = serializers.PrimaryKeyRelatedField(queryset=Symbol.objects.all())

    class Meta:
        model = Future
        fields = ['symbol', 'product_code', 'product_name', 'venue', 'currency','industry', 'contract_size', 'contract_units', 'tick_size', 'min_price_fluctuation', 'continuous']

    def create(self, validated_data):
        # Create the Future instance using validated data
        future = Future.objects.create(**validated_data)
        return future

    def update(self, instance, validated_data):
        # Update fields if present in validated_data or keep existing
        instance.product_code = validated_data.get('product_code', instance.product_code)
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.venue = validated_data.get('venue', instance.venue)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.industry = validated_data.get('industry', instance.industry)
        instance.contract_size = validated_data.get('contract_size', instance.contract_size)
        instance.contract_units = validated_data.get('contract_units', instance.contract_units)
        instance.tick_size = validated_data.get('tick_size', instance.tick_size)
        instance.min_price_fluctuation = validated_data.get('min_price_fluctuation', instance.min_price_fluctuation)
        instance.continuous = validated_data.get('continuous', instance.continuous)
        instance.save()
        return instance
    
class OptionSerializer(serializers.ModelSerializer):
    venue = serializers.SlugRelatedField(slug_field="value", queryset=Venue.objects.all(), required=False)
    currency = serializers.SlugRelatedField(slug_field="value", queryset=Currency.objects.all(), required=False)
    symbol = serializers.PrimaryKeyRelatedField(queryset=Symbol.objects.all())

    class Meta:
        model = Option
        fields = ['symbol','underlying_name', 'expiration_date','strike_price','contract_size','currency', 'venue','option_type']

    def create(self, validated_data):
        # Create the Future instance using validated data
        option = Option.objects.create(**validated_data)
        return option

    def update(self, instance, validated_data):
        # Update fields if present in validated_data or keep existing
        instance.underlying_name = validated_data.get('underlying_name', instance.underlying_name) 
        instance.expiration_date = validated_data.get('expiration_date', instance.expiration_date)
        instance.strike_price = validated_data.get('strike_price', instance.strike_price)
        instance.contract_size = validated_data.get('contract_size', instance.contract_size)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.venue = validated_data.get('venue', instance.venue)
        instance.option_type = validated_data.get('option_type', instance.option_type)
        instance.save()
        return instance

class CryptocurrencySerializer(serializers.ModelSerializer):
    venue = serializers.SlugRelatedField(slug_field="value", queryset=Venue.objects.all(), required=False)
    currency = serializers.SlugRelatedField(slug_field="value", queryset=Currency.objects.all(), required=False)
    symbol = serializers.PrimaryKeyRelatedField(queryset=Symbol.objects.all())

    class Meta:
        model = Cryptocurrency
        fields = ['symbol', 'name', 'venue', 'currrency', 'market_cap',  'circulating_supply','total_supply', 'max_supply']

    def create(self, validated_data):
        crypto = Cryptocurrency.objects.create(**validated_data)
        return crypto

    def update(self, instance, validated_data):
        # Update fields if present in validated_data or keep existing
        instance.name = validated_data.get('name', instance.name) 
        instance.venue = validated_data.get('venue', instance.venue)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.market_cap = validated_data.get('market_cap', instance.market_cap)
        instance.circulating_supply = validated_data.get('circulating_supply', instance.circulating_supply)
        instance.total_supply = validated_data.get('total_supply', instance.total_supply)
        instance.max_supply = validated_data.get('max_supply', instance.max_supply)
        instance.save()
        return instance
    
class IndexSerializer(serializers.ModelSerializer):
    currency = serializers.SlugRelatedField(slug_field="value", queryset=Currency.objects.all(), required=False)
    venue = serializers.SlugRelatedField(slug_field="value", queryset=Venue.objects.all(), required=False)
    asset_class = serializers.SlugRelatedField(slug_field="value", queryset=AssetClass.objects.all(), required=False)
    symbol = serializers.PrimaryKeyRelatedField(queryset=Symbol.objects.all())
    class Meta:
        model = Index
        fields = ['symbol','name', 'currency','asset_class', 'venue']

    def create(self, validated_data):
        index = Index.objects.create(**validated_data)
        return index

    def update(self, instance, validated_data):
        # Update fields if present in validated_data or keep existing
        instance.name = validated_data.get('name', instance.name) 
        instance.currency = validated_data.get('currency', instance.currency)
        instance.asset_class = validated_data.get('asset_class', instance.asset_class)
        instance.venue = validated_data.get('venue', instance.venue)
        instance.save()
        return instance

