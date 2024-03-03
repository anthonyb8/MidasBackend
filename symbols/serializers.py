from rest_framework import serializers
from .models import Symbol, Equity, Cryptocurrency, Future, Option, AssetClass, Currency, Index
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

class SymbolReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = ['id', 'ticker', 'security_type', 'created_at', 'updated_at']

class SymbolWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = ['id', 'ticker', 'security_type', 'created_at', 'updated_at']

class IndexSerializer(serializers.ModelSerializer):
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
    
    symbol_data = SymbolWriteSerializer(write_only=True)
    ticker = serializers.SerializerMethodField()
    asset_class_name = serializers.SerializerMethodField()
    currency_code = serializers.SerializerMethodField()

    class Meta:
        model = Index
        fields = ['symbol_data','ticker', 'name', 'asset_class', 'currency', 'asset_class_name', 'currency_code']

    def get_asset_class_name(self, obj):
        return obj.asset_class.name if obj.asset_class else None
    
    def get_ticker(self, obj):
        return obj.symbol.ticker if obj.symbol else None

    def get_currency_code(self, obj):
        return obj.currency.code if obj.currency else None

    def create(self, validated_data):
        logger.info("Attempting to create a new Index.")
        try:
            # Create associated symbol
            symbol_data = validated_data.pop('symbol_data')
            symbol = Symbol.objects.create(**symbol_data)
            logger.info(f"Symbol sucessfully created: {symbol}")
            
            # Create benchmark and link to symbol
            index = Index.objects.create(symbol=symbol, **validated_data)
            logger.info(f"Index created with ID: {index.id}")
            return index
        except AssetClass.DoesNotExist as e:
            logger.info(e)
            raise APIException("The specified asset class does not exist.")
        except Currency.DoesNotExist:
            logger.info(e)
            raise APIException("The specified currency does not exist.")
        except Exception as e:
            logger.error(f"Failed to create Index: {e}")
            raise APIException(f"Failed to create Index due to an error: {str(e)}")

    def update(self, instance, validated_data):
        """
        Custom update method for Benchmark instances.
        Allows switching to a different AssetClass or Currency without editing them directly.
        """
        logger.info(f"Attempting to update Index with ID: {instance.id}")
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
            logger.info(f"Index updated successfully with ID: {instance.id}")
            return instance
        except Exception as e:
            logger.error(f"Failed to update Index with ID: {instance.id}: {e}")
            raise serializers.ValidationError(f"Failed to update Index due to an error: {str(e)}")

class EquitySerializer(serializers.ModelSerializer):
    symbol_data = SymbolWriteSerializer(write_only=True)
    ticker = serializers.SerializerMethodField()

    class Meta:
        model = Equity
        fields = ['symbol_data','ticker', 'company_name', 'exchange', 'currency', 'industry', 'market_cap', 'shares_outstanding', 'created_at', 'updated_at']
    
    def get_ticker(self, obj):
        return obj.symbol.ticker if obj.symbol else None

    def create(self, validated_data):
        """
        Custom create method for Equity instances.
        Extracts symbol_data, creates a Symbol instance, and then creates an Equity instance.
        """
        logger.info("Attempting to create new Equity with data: %s", validated_data)
        try:
            # Create Symbol
            symbol_data = validated_data.pop('symbol_data')
            symbol = Symbol.objects.create(**symbol_data)
            logger.info(f"Symbol created with ticker: {symbol.ticker}")

            # Create Equity
            equity = Equity.objects.create(symbol=symbol, **validated_data)
            logger.info(f"Equity created with ID: {equity.id}")
            return equity
        except Exception as e:
            logger.error(f"Failed to create Equity: {e}")
            raise serializers.ValidationError(f"Failed to create Equity: {e}")

    def update(self, instance, validated_data):
        """
        Custom update method for Equity instances.
        Optionally updates nested symbol_data if provided, then updates the Equity instance.
        """
        logger.info(f"Attempting to update Equity with ID: {instance.id}")
        
        try:
            symbol_data = validated_data.pop('symbol_data', None)

            # Update Symbol instance if provided
            if symbol_data:
                symbol = instance.symbol
                for attr, value in symbol_data.items():
                    setattr(symbol, attr, value)
                symbol.save()
                logger.info(f"Symbol updated for Equity ID: {instance.id}")

            # Update Equity instance with any remaining validated_data
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            logger.info(f"Equity updated successfully with ID: {instance.id}")
            return instance
        except Exception as e:
            logger.error(f"Failed to update Equity with ID: {instance.id}: {e}")
            raise serializers.ValidationError(f"Failed to update Equity: {e}")

class FutureSerializer(serializers.ModelSerializer):
    symbol_data = SymbolWriteSerializer(write_only=True)
    ticker = serializers.SerializerMethodField()

    class Meta:
        model = Future
        fields = ['symbol_data','ticker','product_code','product_name', 'exchange','currency','contract_size','contract_units','tick_size','min_price_fluctuation', 'continuous','created_at','updated_at']

    def get_ticker(self, obj):
        return obj.symbol.ticker if obj.symbol else None
    
    def create(self, validated_data):
        """
        Custom create method for Future instances.
        Extracts symbol_data, creates a Symbol instance, and then creates an Future instance.
        """
        logger.info("Attempting to create new Future with data: %s", validated_data)
        try:
            # Create Symbol
            symbol_data = validated_data.pop('symbol_data')
            symbol = Symbol.objects.create(**symbol_data)
            logger.info(f"Symbol created with ticker: {symbol.ticker}")

            # Create Future
            future = Future.objects.create(symbol=symbol, **validated_data)
            logger.info(f"Future created with ID: {future.id}")
            return future
        except Exception as e:
            logger.error(f"Failed to create Future: {e}")
            raise serializers.ValidationError(f"Failed to create Future: {e}")
        
    def update(self, instance, validated_data):
        """
        Custom update method for Future instances.
        Optionally updates nested symbol_data if provided, then updates the Future instance.
        """
        logger.info(f"Attempting to update Future with ID: {instance.id}")
        
        try:
            symbol_data = validated_data.pop('symbol_data', None)

            # Update Symbol instance if provided
            if symbol_data:
                symbol = instance.symbol
                for attr, value in symbol_data.items():
                    setattr(symbol, attr, value)
                symbol.save()
                logger.info(f"Symbol updated for Future ID: {instance.id}")

            # Update Future instance with any remaining validated_data
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            logger.info(f"Future updated successfully with ID: {instance.id}")
            return instance
        except Exception as e:
            logger.error(f"Failed to update Future with ID: {instance.id}: {e}")
            raise serializers.ValidationError(f"Failed to update Future: {e}")

class CryptocurrencySerializer(serializers.ModelSerializer):
    symbol_data = SymbolWriteSerializer(write_only=True)
    ticker = serializers.SerializerMethodField()

    class Meta:
        model = Cryptocurrency
        fields = ['symbol_data','ticker', 'cryptocurrency_name', 'circulating_supply', 'market_cap', 'total_supply', 'max_supply', 'description', 'created_at', 'updated_at']
    
    def get_ticker(self, obj):
        return obj.symbol.ticker if obj.symbol else None
    
    def create(self, validated_data):
        """
        Custom create method for Cryptocurrency instances.
        Extracts symbol_data, creates a Symbol instance, and then creates an Cryptocurrency instance.
        """
        logger.info("Attempting to create new Cryptocurrency with data: %s", validated_data)
        try:
            # Create Symbol
            symbol_data = validated_data.pop('symbol_data')
            symbol = Symbol.objects.create(**symbol_data)
            logger.info(f"Symbol created with ticker: {symbol.ticker}")

            # Create Cryptocurrency
            cryptocurrency = Cryptocurrency.objects.create(symbol=symbol, **validated_data)
            logger.info(f"Cryptocurrency created with ID: {cryptocurrency.id}")
            return cryptocurrency
        except Exception as e:
            logger.error(f"Failed to create Cryptocurrency: {e}")
            raise serializers.ValidationError(f"Failed to create Cryptocurrency: {e}")
        
    def update(self, instance, validated_data):
        """
        Custom update method for Cryptocurrency instances.
        Optionally updates nested symbol_data if provided, then updates the Cryptocurrency instance.
        """
        logger.info(f"Attempting to update Cryptocurrency with ID: {instance.id}")
        
        try:
            symbol_data = validated_data.pop('symbol_data', None)

            # Update Symbol instance if provided
            if symbol_data:
                symbol = instance.symbol
                for attr, value in symbol_data.items():
                    setattr(symbol, attr, value)
                symbol.save()
                logger.info(f"Symbol updated for Cryptocurrency ID: {instance.id}")

            # Update Cryptocurrency instance with any remaining validated_data
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            logger.info(f"Cryptocurrency updated successfully with ID: {instance.id}")
            return instance
        except Exception as e:
            logger.error(f"Failed to update Cryptocurrency with ID: {instance.id}: {e}")
            raise serializers.ValidationError(f"Failed to update Cryptocurrency: {e}")

class OptionSerializer(serializers.ModelSerializer):
    symbol_data = SymbolWriteSerializer(write_only=True)
    ticker = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = ['symbol_data','ticker', 'strike_price', 'expiration_date', 'option_type', 'contract_size','underlying_name','exchange','created_at','updated_at']
    
    def get_ticker(self, obj):
        return obj.symbol.ticker if obj.symbol else None
    
    def create(self, validated_data):
        """
        Custom create method for Option instances.
        Extracts symbol_data, creates a Symbol instance, and then creates an Option instance.
        """
        logger.info("Attempting to create new Option with data: %s", validated_data)
        try:
            # Create Symbol
            symbol_data = validated_data.pop('symbol_data')
            symbol = Symbol.objects.create(**symbol_data)
            logger.info(f"Symbol created with ticker: {symbol.ticker}")

            # Create Option
            option = Option.objects.create(symbol=symbol, **validated_data)
            logger.info(f"Option created with ID: {option.id}")
            return option
        except Exception as e:
            logger.error(f"Failed to create Option: {e}")
            raise serializers.ValidationError(f"Failed to create Option: {e}")

    def update(self, instance, validated_data):
        """
        Custom update method for Option instances.
        Optionally updates nested symbol_data if provided, then updates the Option instance.
        """
        logger.info(f"Attempting to update Option with ID: {instance.id}")
        
        try:
            symbol_data = validated_data.pop('symbol_data', None)

            # Update Symbol instance if provided
            if symbol_data:
                symbol = instance.symbol
                for attr, value in symbol_data.items():
                    setattr(symbol, attr, value)
                symbol.save()
                logger.info(f"Symbol updated for Option ID: {instance.id}")

            # Update Option instance with any remaining validated_data
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            logger.info(f"Option updated successfully with ID: {instance.id}")
            return instance
        except Exception as e:
            logger.error(f"Failed to update Option with ID: {instance.id}: {e}")
            raise serializers.ValidationError(f"Failed to update Option: {e}")


    
