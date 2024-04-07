from rest_framework import serializers
from .models import Session, Position, Account, Order, Risk, MarketData

class CreateSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['session_id']

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'session', 'data']
        extra_kwargs = {'session': {'read_only': True}}

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'session', 'data']
        extra_kwargs = {'session': {'read_only': True}}

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'session', 'data']
        extra_kwargs = {'session': {'read_only': True}}

class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = ['id', 'session', 'data']
        extra_kwargs = {'session': {'read_only': True}}

class MarketDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketData
        fields = ['id', 'session', 'data']
        extra_kwargs = {'session': {'read_only': True}}

class SessionDetailSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(read_only=True)
    orders = OrderSerializer(read_only=True)
    risk = RiskSerializer(read_only=True)
    market_data = MarketDataSerializer(read_only=True)
    account = AccountSerializer(read_only=True)

    class Meta:
        model = Session
        fields = ['session_id', 'positions', 'account', 'orders', 'risk', 'market_data']
