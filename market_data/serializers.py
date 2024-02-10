from rest_framework import serializers
from django.db import transaction
from .models import BarData
from symbols.models import Symbol

class BarDataSerializer(serializers.ModelSerializer):
    symbol = serializers.SlugRelatedField(
        queryset=Symbol.objects.all(),
        slug_field='ticker',
        write_only=False  # Allowing both read and write
    )

    class Meta:
        model = BarData
        fields = ['id', 'symbol', 'timestamp', 'open', 'close', 'high', 'low', 'volume']

    def to_representation(self, instance):
        """Modify the representation for read operations to include the ticker."""
        ret = super().to_representation(instance)
        # Ensure 'symbol' shows the ticker symbol, not the Symbol object ID
        ret['symbol'] = instance.symbol.ticker
        return ret

    def create(self, validated_data):
        # Handle bulk create if validated_data is a list
        if isinstance(validated_data, list):
            with transaction.atomic():  # Ensures all-or-nothing for bulk operations
                instances = [BarData(**item) for item in validated_data]
                return BarData.objects.bulk_create(instances)
        else:
            # For single instance creation, just use the standard create
            return super().create(validated_data)

    def update(self, instance, validated_data):
        # 'ticker' field is automatically handled by SlugRelatedField
        return super().update(instance, validated_data)










# from rest_framework import serializers
# from .models import BarData
# from symbols.models import Symbol

# class BarDataSerializer(serializers.ModelSerializer):
#     symbol = serializers.SlugRelatedField(
#         queryset=Symbol.objects.all(),
#         slug_field='ticker', 
#         write_only=False  # Now allowing both read and write
#     )

#     class Meta:
#         model = BarData
#         fields = ['id', 'symbol', 'timestamp', 'open', 'close', 'high', 'low', 'volume']

#     def to_representation(self, instance):
#         """Modify the representation for read operations to include the ticker."""
#         ret = super().to_representation(instance)
#         # Ensure 'ticker' shows the ticker symbol, not the Symbol object ID
#         ret['symbol'] = instance.symbol.ticker
#         return ret

#     def create(self, validated_data):
#         # 'ticker' field is automatically handled by SlugRelatedField
#         return super().create(validated_data)

#     def update(self, instance, validated_data):
#         # 'ticker' field is automatically handled by SlugRelatedField
#         return super().update(instance, validated_data)


