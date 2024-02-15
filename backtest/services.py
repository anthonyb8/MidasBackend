from django.db import transaction
from .models import Backtest, StaticStats, TimeseriesStats, Trade, Signal, TradeInstruction

def create_backtest(validated_data):
    with transaction.atomic():
        # Create the Backtest instance
        # backtest = Backtest.objects.create(**validated_data)
        static_stats_data = validated_data.pop('static_stats', [])
        timeseries_stats_data = validated_data.pop('timeseries_stats', [])
        trades_data = validated_data.pop('trades', [])
        signals_data = validated_data.pop('signals', [])

        # # Create the Backtest instance
        backtest = Backtest.objects.create(**validated_data)

        # Nested object creation for SummaryStats
        for stat_data in static_stats_data:
            StaticStats.objects.create(backtest=backtest, **stat_data)

        # Nested object creation for TimeseriesStats
        for stat_data in timeseries_stats_data:
            TimeseriesStats.objects.create(backtest=backtest, **stat_data)

        # Nested object creation for Trades
        for trade_data in trades_data:
            Trade.objects.create(backtest=backtest, **trade_data)

        # Nested object creation for Signals and their TradeInstructions
        for signal_data in signals_data:
            trade_instructions_data = signal_data.pop('trade_instructions', [])
            signal_instance = Signal.objects.create(backtest=backtest, **signal_data)
            for ti_data in trade_instructions_data:
                TradeInstruction.objects.create(signal=signal_instance, **ti_data)

        return backtest
