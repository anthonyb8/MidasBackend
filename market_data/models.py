from django.db import models
from symbols.models import Symbol

class BarData(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='bardata')
    timestamp = models.BigIntegerField(db_index=True) 
    open = models.DecimalField(max_digits=10, decimal_places=4)
    close = models.DecimalField(max_digits=10, decimal_places=4)
    high = models.DecimalField(max_digits=10, decimal_places=4)
    low = models.DecimalField(max_digits=10, decimal_places=4)
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('symbol', 'timestamp')
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['symbol', 'timestamp']), # Composite index for optimizing queries
        ]


    def __str__(self):
        return f"BarData(ticker={self.symbol}, timestamp={self.timestamp})"

class QuoteData(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='quotedata')
    timestamp = models.BigIntegerField(db_index=True)
    ask = models.DecimalField(max_digits=10, decimal_places=4)
    ask_size = models.DecimalField(max_digits=10, decimal_places=4)
    bid = models.DecimalField(max_digits=10, decimal_places=4)
    bid_size = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        unique_together = ('symbol', 'timestamp')
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['symbol', 'timestamp']), # Composite index for optimizing queries
        ]


    def __str__(self):
        return f"BarData(ticker={self.symbol}, timestamp={self.timestamp})"


