from rest_framework import serializers
from .models import Symbol, Equity, Cryptocurrency, Future, Option, AssetClass, Currency, Benchmark
from rest_framework.exceptions import APIException
import logging

logger = logging.getLogger(__name__)

class AssetClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetClass
        fields = ['id', 'name', 'description']

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name', 'region']

class SymbolWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = ['id', 'ticker', 'security_type', 'created_at', 'updated_at']

class BenchmarkSerializer(serializers.ModelSerializer):
    asset_class = serializers.SlugRelatedField(
        slug_field='name',
        queryset=AssetClass.objects.all(),
        write_only=True
    )
    currency = serializers.SlugRelatedField(
        slug_field='code',
        queryset=Currency.objects.all(),
        write_only=True
    )
    
    asset_class_name = serializers.SerializerMethodField()
    currency_code = serializers.SerializerMethodField()
    symbol_data = SymbolWriteSerializer(write_only=True)

    class Meta:
        model = Benchmark
        fields = ['symbol_data', 'benchmark_name', 'asset_class', 'currency', 'asset_class_name', 'currency_code']

    def get_asset_class_name(self, obj):
        return obj.asset_class.name if obj.asset_class else None

    def get_currency_code(self, obj):
        return obj.currency.code if obj.currency else None

    def create(self, validated_data):
        try:
            # Create associated symbol
            symbol_data = validated_data.pop('symbol_data')
            symbol = Symbol.objects.create(**symbol_data)
            logger.info(f"Symbol sucessfully created: {symbol}")
            
            # Create benchmark and link to symbol
            benchmark = Benchmark.objects.create(ticker=symbol, **validated_data)
            logger.info(f"Benchmark sucessfully created: {benchmark}")
            
            return benchmark
        except AssetClass.DoesNotExist as e:
            logger.info(e)
            raise APIException("The specified asset class does not exist.")
        except Currency.DoesNotExist:
            logger.info(e)
            raise APIException("The specified currency does not exist.")
        except Exception as e:
            logger.info(f"Failed to create benchmark: {str(e)}")
            raise APIException(f"Failed to create benchmark: {str(e)}")

    def update(self, instance, validated_data):
        """
        Custom update method for Benchmark instances.
        Allows switching to a different AssetClass or Currency without editing them directly.
        """
        try:
            # Optional: Update Symbol data if provided
            symbol_obj = validated_data.pop('symbol_data', None)
            if symbol_obj:
                symbol = instance.ticker
                for attr, value in symbol_obj.items():
                    setattr(symbol, attr, value)
                symbol.save()

            # Optional: Update AssetClass if a new name is provided
            asset_class_obj = validated_data.pop('asset_class', None)
            if asset_class_obj:
                try:
                    # asset_class = AssetClass.objects.get(name=asset_class_name)
                    instance.asset_class = asset_class_obj
                except AssetClass.DoesNotExist:
                    raise APIException("The specified asset class does not exist.")

            # Optional: Update Currency if a new code is provided
            currency_obj = validated_data.pop('currency', None)
            if currency_obj:
                try:
                    # currency = Currency.objects.get(code=currency_code)
                    instance.currency = currency_obj
                except Currency.DoesNotExist:
                    raise APIException("The specified currency does not exist.")

            # Save any other updated fields of the Benchmark instance
            instance.save()

            return instance
        except Exception as e:
            logger.error(f"Error in update: {str(e)}")
            raise APIException("Failed to update benchmark.")

class EquitySerializer(serializers.ModelSerializer):
    # Use SymbolWriteSerializer to handle the nested symbol data for write operations
    symbol_data = SymbolWriteSerializer(write_only=True)

    class Meta:
        model = Equity
        fields = ['symbol_data', 'company_name', 'exchange', 'currency', 'industry', 'market_cap', 'shares_outstanding', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        Custom create method for Equity instances.
        Extracts symbol_data, creates a Symbol instance, and then creates an Equity instance.
        """
        try:
            # Extract symbol_data from the validated data
            symbol_data = validated_data.pop('symbol_data')
            # Create a new Symbol instance from the symbol_data
            symbol = Symbol.objects.create(**symbol_data)
            # Create and return a new Equity instance, linking it with the created Symbol
            equity = Equity.objects.create(symbol=symbol, **validated_data)
            return equity
        except Exception as e:
            # Log the exception for debugging purposes
            logger.error(f"Error in create: {str(e)}")
            # Raise a generic APIException for any errors encountered during creation
            raise APIException("Failed to create equity. Please check your data.")

    def update(self, instance, validated_data):
        """
        Custom update method for Equity instances.
        Optionally updates nested symbol_data if provided, then updates the Equity instance.
        """
        # Optionally extract symbol_data for update, defaulting to None if not provided
        symbol_data = validated_data.pop('symbol_data', None)

        # If symbol_data is provided, update the related Symbol instance
        if symbol_data:
            symbol = instance.symbol
            for attr, value in symbol_data.items():
                setattr(symbol, attr, value)
            symbol.save()

        # Update the Equity instance with any remaining validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class FutureSerializer(serializers.ModelSerializer):
    symbol_data = SymbolWriteSerializer(write_only=True)

    class Meta:
        model = Future
        fields = ['symbol_data','product_code','product_name', 'exchange','currency','contract_size','contract_units','tick_size','min_price_fluctuation', 'continuous','created_at','updated_at']

    def create(self, validated_data):
        symbol_data = validated_data.pop('symbol_data')
        symbol = Symbol.objects.create(**symbol_data)
        future = Future.objects.create(symbol=symbol, **validated_data)
        return future

    def update(self, instance, validated_data):
        symbol_data = validated_data.pop('symbol_data', None)
        symbol = instance.symbol

        # Update the symbol instance
        if symbol_data:
            for attr, value in symbol_data.items():
                setattr(symbol, attr, value)
            symbol.save()

        # Update the Equity instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class CryptocurrencySerializer(serializers.ModelSerializer):
    symbol_data = SymbolWriteSerializer(write_only=True)

    class Meta:
        model = Cryptocurrency
        fields = ['symbol_data', 'cryptocurrency_name', 'circulating_supply', 'market_cap', 'total_supply', 'max_supply', 'description', 'created_at', 'updated_at']

    def create(self, validated_data):
        symbol_data = validated_data.pop('symbol_data')
        symbol = Symbol.objects.create(**symbol_data)
        cryptocurrency = Cryptocurrency.objects.create(symbol=symbol, **validated_data)
        return cryptocurrency

    def update(self, instance, validated_data):
        symbol_data = validated_data.pop('symbol_data', None)
        symbol = instance.symbol

        # Update the symbol instance
        if symbol_data:
            for attr, value in symbol_data.items():
                setattr(symbol, attr, value)
            symbol.save()

        # Update the Equity instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class OptionSerializer(serializers.ModelSerializer):
    symbol_data = SymbolWriteSerializer(write_only=True)

    class Meta:
        model = Option
        fields = ['symbol_data', 'strike_price', 'expiration_date', 'option_type', 'contract_size','underlying_name','exchange','created_at','updated_at']

    def create(self, validated_data):
        symbol_data = validated_data.pop('symbol_data')
        symbol = Symbol.objects.create(**symbol_data)
        option = Option.objects.create(symbol=symbol, **validated_data)
        return option

    def update(self, instance, validated_data):
        symbol_data = validated_data.pop('symbol_data', None)
        symbol = instance.symbol

        # Update the symbol instance
        if symbol_data:
            for attr, value in symbol_data.items():
                setattr(symbol, attr, value)
            symbol.save()

        # Update the Equity instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
    
class SymbolReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = ['id', 'ticker', 'security_type', 'created_at', 'updated_at']

    def to_representation(self, instance):
        """Customize the serialization based on the symbol type."""
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
    
