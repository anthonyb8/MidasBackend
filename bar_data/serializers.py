from rest_framework import serializers
from .models import BarData
from assets.models import Asset 

class BarDataSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(write_only=True)

    class Meta:
        model = BarData
        fields = ['id', 'symbol', 'timestamp', 'open', 'close', 'high', 'low', 'volume']

    def to_representation(self, instance):
        """Modify the representation for read operations to include the symbol."""
        ret = super().to_representation(instance)
        ret['symbol'] = instance.asset.symbol
        return ret

    def create(self, validated_data):
        # Convert symbol to asset
        asset = self.get_asset_by_symbol(validated_data.pop('symbol'))
        print(f'asset:\n{asset}')
        validated_data['asset'] = asset
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Convert symbol to asset
        asset = self.get_asset_by_symbol(validated_data.pop('symbol'))
        validated_data['asset'] = asset
        return super().update(instance, validated_data)

    @staticmethod
    def get_asset_by_symbol(symbol):
        try:
            return Asset.objects.get(symbol=symbol)
        except Asset.DoesNotExist:
            raise serializers.ValidationError(f"Asset with symbol {symbol} does not exist")
