from rest_framework import serializers
from .models import BarData
from symbols.models import Symbol

class BarDataSerializer(serializers.ModelSerializer):
    ticker = serializers.SlugRelatedField(
        queryset=Symbol.objects.all(),
        slug_field='ticker',  # Assuming 'ticker' is the field on Symbol you want to relate by
        write_only=False  # Now allowing both read and write
    )

    class Meta:
        model = BarData
        fields = ['id', 'ticker', 'timestamp', 'open', 'close', 'high', 'low', 'volume']

    def to_representation(self, instance):
        """Modify the representation for read operations to include the ticker."""
        ret = super().to_representation(instance)
        # Ensure 'ticker' shows the ticker symbol, not the Symbol object ID
        ret['ticker'] = instance.ticker.ticker
        return ret

    def create(self, validated_data):
        # 'ticker' field is automatically handled by SlugRelatedField
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # 'ticker' field is automatically handled by SlugRelatedField
        return super().update(instance, validated_data)








# from rest_framework import serializers
# from .models import BarData
# from symbols.models import Symbol

# class BarDataSerializer(serializers.ModelSerializer):
#     symbol = serializers.CharField(write_only=True)

#     class Meta:
#         model = BarData
#         fields = ['id', 'ticker', 'timestamp', 'open', 'close', 'high', 'low', 'volume']

#     def to_representation(self, instance):
#         """Modify the representation for read operations to include the symbol."""
#         ret = super().to_representation(instance)
#         ret['symbol'] = instance.symbol.ticker
#         return ret

#     def create(self, validated_data):
#         # Convert symbol to symbol
#         symbol = self.get_symbol_by_symbol(validated_data.pop('symbol'))
#         validated_data['symbol'] = symbol
#         return super().create(validated_data)

#     def update(self, instance, validated_data):
#         # Convert symbol to symbol
#         symbol = self.get_symbol_by_symbol(validated_data.pop('symbol'))
#         validated_data['symbol'] = symbol
#         return super().update(instance, validated_data)

#     @staticmethod
#     def get_symbol_by_symbol(symbol):
#         try:
#             return Symbol.objects.get(symbol=symbol)
#         except Symbol.DoesNotExist:
#             raise serializers.ValidationError(f"Symbol with symbol {symbol} does not exist")
