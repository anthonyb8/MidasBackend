from rest_framework import serializers
from .models import Backtest, StaticStats, TimeseriesStats, Trade, Signal, TradeInstruction
from .services import create_backtest


class StaticStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticStats
        fields = [
                    'net_profit', 'total_return','max_drawdown','annual_standard_deviation','ending_equity', 
                    'total_fees', 'total_trades', "num_winning_trades", "num_lossing_trades", "avg_win_percent", 
                    "avg_loss_percent","percent_profitable", "profit_and_loss", "profit_factor", "avg_trade_profit", 
                    'sharpe_ratio', 'sortino_ratio', 'alpha', 'beta'
                ]

class TimeseriesStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeseriesStats
        fields = ['timestamp', 'equity_value', 'percent_drawdown', 'cumulative_return', 'daily_return']


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ['trade_id', 'leg_id', 'timestamp', 'symbol', 'quantity', 'price', 'cost', 'action', 'fees']


class TradeInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeInstruction
        fields = ['ticker', 'action', 'trade_id', 'leg_id', 'weight']

class SignalSerializer(serializers.ModelSerializer):
    trade_instructions = TradeInstructionSerializer(many=True)

    class Meta:
        model = Signal
        fields = ['timestamp', 'trade_instructions']

    def create(self, validated_data):
        trade_instructions_data = validated_data.pop('trade_instructions', [])
        signal = Signal.objects.create(**validated_data)
        for ti_data in trade_instructions_data:
            TradeInstruction.objects.create(signal=signal, **ti_data)
        return signal

class BacktestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backtest
        fields = ['id', 'strategy_name', 'tickers', 'benchmark', 'data_type', 'train_start', 'train_end', 'test_start', 'test_end', 'capital', 'strategy_allocation', 'created_at']

class BacktestSerializer(serializers.ModelSerializer):
    parameters = BacktestListSerializer(source='*') 
    timeseries_stats = TimeseriesStatsSerializer(many=True)
    static_stats = StaticStatsSerializer(many=True)
    trades = TradeSerializer(many=True)
    signals = SignalSerializer(many=True)

    class Meta:
        model = Backtest
        fields = ['id', 'parameters', 'static_stats', 'trades', 'timeseries_stats', 'signals']

    def create(self, validated_data):
        # Extract parameters from the initial data if available
        parameters = self.initial_data.get('parameters', {})

        # Map parameters to the respective fields in Backtest model
        validated_data['strategy_name'] = parameters.get('strategy_name')
        validated_data['tickers'] = parameters.get('tickers')
        validated_data['train_start'] = parameters.get('train_start')
        validated_data['train_end'] = parameters.get('train_end')
        validated_data['test_start'] = parameters.get('test_start')
        validated_data['test_end'] = parameters.get('test_end')
        validated_data['capital'] = parameters.get('capital')
        validated_data['strategy_allocation'] = parameters.get('strategy_allocation')

        return create_backtest(validated_data)
