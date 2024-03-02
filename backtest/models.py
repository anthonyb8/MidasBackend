from django.db import models
from market_data.models import BarData
import json


class Backtest(models.Model):
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def fetch_price_data(self):
        # Assuming there's a HistoricalPriceData model or equivalent
        # Fetch price data for the symbols and date range of this backtest
        price_data = BarData.objects.filter(
            symbol__in=self.tickers,
            timestamp__gte=self.test_start,
            timestamp__lte=self.test_end
        ).order_by('timestamp')
        return [data.to_dict() for data in price_data]
        
    def to_dict(self):
        return {
            "parameters": {
                "strategy_name": self.strategy_name,
                "tickers": json.loads(self.tickers),  # Ensure the tickers are returned as a list
                "data_type": self.data_type,
                "strategy_allocation": self.strategy_allocation,
                "capital": self.capital,
                "train_start": self.train_start,
                "train_end": self.train_end,
                "test_start": self.test_start,
                "test_end": self.test_end,
                "benchmark": json.loads(self.benchmark),  # Ensure the benchmark is returned as a list
                "created_at": self.created_at.isoformat(),
            },
            "static_stats": [stat.to_dict() for stat in self.static_stats.all()],
            "timeseries_stats": [ts_stat.to_dict() for ts_stat in self.timeseries_stats.all()],
            "trades": [trade.to_dict() for trade in self.trades.all()],
            "signals": [signal.to_dict() for signal in self.signals.all()],
        }

class Trade(models.Model):
    backtest = models.ForeignKey(Backtest, related_name='trades', on_delete=models.CASCADE)
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
    backtest = models.ForeignKey(Backtest, related_name='signals', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

class TradeInstruction(models.Model):
    signal = models.ForeignKey(Signal, related_name='trade_instructions', on_delete=models.CASCADE)
    ticker = models.CharField(max_length=100)
    action = models.CharField(max_length=10)  # 'BUY' or 'SELL'
    trade_id = models.PositiveIntegerField()
    leg_id = models.PositiveIntegerField()
    weight = models.FloatField()

class StaticStats(models.Model):
    backtest = models.ForeignKey(Backtest, related_name='static_stats', on_delete=models.CASCADE)
    # General Stats
    net_profit = models.FloatField(null=True)
    total_return = models.FloatField(null=True)
    max_drawdown = models.FloatField(null=True)
    annual_standard_deviation = models.FloatField(null=True)
    ending_equity = models.FloatField(null=True)
    total_fees = models.FloatField(null=True)
    # Trade Stats
    total_trades = models.IntegerField(null=True)
    num_winning_trades = models.IntegerField(null=True)
    num_lossing_trades = models.IntegerField(null=True)
    avg_win_percent = models.FloatField(null=True)
    avg_loss_percent = models.FloatField(null=True)
    percent_profitable = models.FloatField(null=True)
    profit_and_loss = models.FloatField(null=True)
    profit_factor = models.FloatField(null=True)
    avg_trade_profit = models.FloatField(null=True)
    # Benchmark Stats
    sharpe_ratio = models.FloatField(null=True)
    sortino_ratio = models.FloatField(null=True)
    alpha = models.FloatField(null=True)
    beta = models.FloatField(null=True)

class TimeseriesStats(models.Model):
    backtest = models.ForeignKey(Backtest, related_name='timeseries_stats', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    equity_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    daily_return = models.DecimalField(max_digits=15, decimal_places=6, default=0.0)
    cumulative_return = models.DecimalField(max_digits=15, decimal_places=6, default=0.0)
    percent_drawdown = models.DecimalField(max_digits=15, decimal_places=6, default=0.0)
