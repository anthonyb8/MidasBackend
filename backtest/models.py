import json
from decimal import Decimal
from django.db import models
from market_data.models import BarData

class Backtest(models.Model):
    strategy_name = models.CharField(max_length=255)
    tickers = models.JSONField(default=list)
    benchmark = models.JSONField(default=list)
    data_type = models.CharField(max_length=10)
    train_start = models.BigIntegerField(null=True, blank=True)
    train_end = models.BigIntegerField(null=True, blank=True)
    test_start = models.BigIntegerField(null=True, blank=True) 
    test_end = models.BigIntegerField(null=True, blank=True)
    capital = models.FloatField(null=True, blank=True)
    strategy_allocation = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Trade(models.Model):
    backtest = models.ForeignKey(Backtest, related_name='trades', on_delete=models.CASCADE)
    trade_id = models.CharField(max_length=100)  
    leg_id = models.CharField(max_length=100)    
    timestamp = models.BigIntegerField(null=True, blank=True)
    ticker = models.CharField(max_length=50)     
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    avg_price = models.DecimalField(max_digits=10, decimal_places=4)
    trade_value = models.DecimalField(max_digits=15, decimal_places=4)
    action = models.CharField(max_length=10)  # Assuming 'direction' is a string like 'buy' or 'sell'
    fees =  models.DecimalField(max_digits=10, decimal_places=4)

class Signal(models.Model):
    backtest = models.ForeignKey(Backtest, related_name='signals', on_delete=models.CASCADE)
    timestamp = models.BigIntegerField(null=True, blank=True)

class TradeInstruction(models.Model):
    signal = models.ForeignKey(Signal, related_name='trade_instructions', on_delete=models.CASCADE)
    ticker = models.CharField(max_length=100)
    action = models.CharField(max_length=10)  # 'BUY' or 'SELL'
    trade_id = models.PositiveIntegerField()
    leg_id = models.PositiveIntegerField()
    weight = models.FloatField()

class StaticStats(models.Model):
    backtest = models.ForeignKey(Backtest, related_name='static_stats', on_delete=models.CASCADE)
    net_profit = models.FloatField(null=True)
    total_fees = models.FloatField(null=True)
    ending_equity = models.FloatField(null=True)
    avg_trade_profit = models.FloatField(null=True)
    total_return = models.FloatField(null=True)
    annual_standard_deviation_percentage = models.FloatField(null=True)
    max_drawdown_percentage = models.FloatField(null=True)
    avg_win_percentage = models.FloatField(null=True)
    avg_loss_percentage = models.FloatField(null=True)
    percent_profitable = models.FloatField(null=True)
    total_trades = models.IntegerField(null=True)
    number_winning_trades = models.IntegerField(null=True)
    number_losing_trades = models.IntegerField(null=True)
    profit_and_loss_ratio = models.FloatField(null=True)
    profit_factor = models.FloatField(null=True)
    sortino_ratio = models.FloatField(null=True)
    sharpe_ratio = models.FloatField(null=True)

class PeriodTimeseriesStats(models.Model):
    backtest = models.ForeignKey(Backtest, related_name='period_timeseries_stats', on_delete=models.CASCADE)
    timestamp = models.BigIntegerField(null=True, blank=True)
    equity_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    period_return = models.DecimalField(max_digits=15, decimal_places=6, default=0.0)
    cumulative_return = models.DecimalField(max_digits=15, decimal_places=6, default=0.0)
    percent_drawdown = models.DecimalField(max_digits=15, decimal_places=6, default=0.0)

class DailyTimeseriesStats(models.Model):
    backtest = models.ForeignKey(Backtest, related_name='daily_timeseries_stats', on_delete=models.CASCADE)
    timestamp = models.BigIntegerField(null=True, blank=True)
    equity_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    period_return = models.DecimalField(max_digits=15, decimal_places=6, default=0.0)
    cumulative_return = models.DecimalField(max_digits=15, decimal_places=6, default=0.0)
    percent_drawdown = models.DecimalField(max_digits=15, decimal_places=6, default=0.0)
