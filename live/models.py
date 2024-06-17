import json
from django.db import models
from market_data.models import BarData

class LiveSession(models.Model):
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

class Signal(models.Model):
    live_session = models.ForeignKey(LiveSession, related_name='signals', on_delete=models.CASCADE)
    timestamp = models.BigIntegerField(null=True, blank=True)

class TradeInstruction(models.Model):
    signal = models.ForeignKey(Signal, related_name='trade_instructions', on_delete=models.CASCADE)
    ticker = models.CharField(max_length=100)
    action = models.CharField(max_length=10)  # 'BUY' or 'SELL'
    trade_id = models.PositiveIntegerField()
    leg_id = models.PositiveIntegerField()
    weight = models.FloatField()

class Trade(models.Model):
    live_session = models.ForeignKey(LiveSession, related_name='trades', on_delete=models.CASCADE)   
    timestamp = models.BigIntegerField(null=True, blank=True)
    ticker = models.CharField(max_length=50)     
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    cost = models.DecimalField(max_digits=10, decimal_places=4)
    action = models.CharField(max_length=10)  # Assuming 'direction' is a string like 'buy' or 'sell'
    fees =  models.DecimalField(max_digits=10, decimal_places=4)
class AccountSummary(models.Model):
    live_session = models.ForeignKey(LiveSession, related_name='account_data', on_delete=models.CASCADE)
    currency = models.CharField(max_length=4)  # 'USD'

    # Starting Snapshot
    start_timestamp = models.BigIntegerField(null=True, blank=True)
    start_buying_power = models.DecimalField(max_digits=15, decimal_places=4)
    start_excess_liquidity = models.DecimalField(max_digits=15, decimal_places=4) 
    start_full_available_funds = models.DecimalField(max_digits=15, decimal_places=4)
    start_full_init_margin_req = models.DecimalField(max_digits=15, decimal_places=4)
    start_full_maint_margin_req = models.DecimalField(max_digits=15, decimal_places=4)
    start_futures_pnl = models.DecimalField(max_digits=15, decimal_places=4)
    start_net_liquidation = models.DecimalField(max_digits=15, decimal_places=4)
    start_total_cash_balance = models.DecimalField(max_digits=15, decimal_places=4)
    start_unrealized_pnl = models.DecimalField(max_digits=15, decimal_places=4) 
    
    # Ending Snapshot
    end_timestamp = models.BigIntegerField(null=True, blank=True)
    end_buying_power = models.DecimalField(max_digits=15, decimal_places=4)
    end_excess_liquidity = models.DecimalField(max_digits=15, decimal_places=4) 
    end_full_available_funds = models.DecimalField(max_digits=15, decimal_places=4)
    end_full_init_margin_req = models.DecimalField(max_digits=15, decimal_places=4)
    end_full_maint_margin_req = models.DecimalField(max_digits=15, decimal_places=4)
    end_futures_pnl = models.DecimalField(max_digits=15, decimal_places=4)
    end_net_liquidation = models.DecimalField(max_digits=15, decimal_places=4)
    end_total_cash_balance = models.DecimalField(max_digits=15, decimal_places=4)
    end_unrealized_pnl = models.DecimalField(max_digits=16, decimal_places=4) 
