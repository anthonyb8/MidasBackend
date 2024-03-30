import json
from django.db import models
from market_data.models import BarData

class LiveSession(models.Model):
    strategy_name = models.CharField(max_length=255)
    tickers = models.JSONField(default=list)
    benchmark = models.JSONField(default=list)
    data_type = models.CharField(max_length=10)
    train_start = models.CharField(max_length=25, null=True, blank=True)
    train_end = models.CharField(max_length=25, null=True, blank=True)
    test_start = models.CharField(max_length=25, null=True, blank=True)
    test_end =  models.CharField(max_length=25, null=True, blank=True)
    capital = models.FloatField(null=True, blank=True)
    strategy_allocation = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Trade(models.Model):
    live_session = models.ForeignKey(LiveSession, related_name='trades', on_delete=models.CASCADE)
    trade_id = models.CharField(max_length=100)  
    leg_id = models.CharField(max_length=100)    
    timestamp = models.DateTimeField()
    ticker = models.CharField(max_length=50)     
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    cost = models.DecimalField(max_digits=10, decimal_places=4)
    action = models.CharField(max_length=10)  # Assuming 'direction' is a string like 'buy' or 'sell'
    fees =  models.DecimalField(max_digits=10, decimal_places=4)

class Signal(models.Model):
    live_session = models.ForeignKey(LiveSession, related_name='signals', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

class TradeInstruction(models.Model):
    signal = models.ForeignKey(Signal, related_name='trade_instructions', on_delete=models.CASCADE)
    ticker = models.CharField(max_length=100)
    action = models.CharField(max_length=10)  # 'BUY' or 'SELL'
    trade_id = models.PositiveIntegerField()
    leg_id = models.PositiveIntegerField()
    weight = models.FloatField()

class SummaryStats(models.Model):
    live_session = models.ForeignKey(LiveSession, related_name='summary_stats', on_delete=models.CASCADE)
    ending_equity = models.FloatField(null=True)
    total_fees = models.FloatField(null=True)
    unrealized_pnl = models.FloatField(null=True)
    realized_pnl = models.FloatField(null=True)
