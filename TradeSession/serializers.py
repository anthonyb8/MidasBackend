from rest_framework import serializers

class PositionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['BUY', 'SELL'])
    avg_cost = serializers.FloatField()
    quantity = serializers.IntegerField()
    total_cost = serializers.FloatField()
    market_value = serializers.FloatField()
    multiplier = serializers.IntegerField()
    initial_margin = serializers.FloatField()

    ticker = serializers.CharField(max_length=10)
    price = serializers.FloatField(required=False)

class OrderSerializer(serializers.Serializer):
    permId = serializers.IntegerField()
    clientId = serializers.IntegerField()
    orderId = serializers.IntegerField()
    parentId = serializers.IntegerField()
    account = serializers.CharField(max_length=20)
    symbol = serializers.CharField(max_length=10)
    secType = serializers.CharField(max_length=20)
    exchange = serializers.CharField(max_length=20)
    action = serializers.ChoiceField(choices=['BUY', 'SELL'])
    orderType = serializers.CharField(max_length=20)
    totalQty = serializers.FloatField()
    cashQty = serializers.FloatField()
    lmtPrice = serializers.FloatField()
    auxPrice = serializers.FloatField()
    status = serializers.CharField(max_length=15)
    filled = serializers.CharField(max_length=15)
    remaining = serializers.FloatField()
    avgFillPrice = serializers.FloatField()
    lastFillPrice = serializers.FloatField()
    whyHeld = serializers.CharField(max_length=15,allow_blank=True)
    mktCapPrice = serializers.FloatField()

class AccountSerializer(serializers.Serializer):
    Timestamp = serializers.CharField(max_length=20)
    FullAvailableFunds = serializers.FloatField()
    FullInitMarginReq = serializers.FloatField()
    NetLiquidation = serializers.FloatField()
    UnrealizedPnL = serializers.FloatField()
    FullMaintMarginReq = serializers.FloatField()
    ExcessLiquidity = serializers.FloatField()
    Currency = serializers.CharField(max_length=3)
    BuyingPower = serializers.FloatField()
    FuturesPNL = serializers.FloatField()
    TotalCashBalance = serializers.FloatField()

class RiskModelSerializer(serializers.Serializer):
    model_id = serializers.CharField(max_length=20)
    risk_level = serializers.CharField(max_length=10)
    # Include further fields relevant to your risk model

class MarketDataSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=10)
    last_price = serializers.FloatField()
    volume = serializers.IntegerField()