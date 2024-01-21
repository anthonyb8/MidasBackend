from django.db import models

class BarData(models.Model):
    asset = models.ForeignKey('assets.Asset', on_delete=models.CASCADE, related_name='bardata')
    timestamp = models.DateTimeField()
    open = models.DecimalField(max_digits=10, decimal_places=4)
    close = models.DecimalField(max_digits=10, decimal_places=4)
    high = models.DecimalField(max_digits=10, decimal_places=4)
    low = models.DecimalField(max_digits=10, decimal_places=4)
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('asset', 'timestamp')
        ordering = ['timestamp']

    def __str__(self):
        return f"BarData(asset={self.asset}, timestamp={self.timestamp})"


