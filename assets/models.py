from django.db import models

class Asset(models.Model):
    SECURITY_TYPES = (
        ('EQUITY', 'EQUITY'),
        ('FUTURE', 'FUTURE'),
        ('OPTION', 'OPTION'),
    )
    symbol = models.CharField(max_length=10, unique=True)
    security_type = models.CharField(max_length=10, choices=SECURITY_TYPES) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.security_type == 'EQUITY':
            self.symbol = self.symbol.upper()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('symbol', 'security_type')

    def __str__(self):
        return f"Asset(symbol={self.symbol}, security_type={self.security_type})"
    
class Equity(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='equity')
    company_name = models.CharField(max_length=150)
    exchange = models.CharField(max_length=25)
    currency = models.CharField(max_length=3)
    industry = models.CharField(max_length=50, default='NULL')
    market_cap = models.IntegerField(null=True, blank=True)
    shares_outstanding = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Equity(company_name={self.company_name}, exchange={self.exchange})"
    
class Future(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='future')
    product_code = models.CharField(max_length=10)  # Example: ZC
    product_name = models.CharField(max_length=50)
    exchange = models.CharField(max_length=25)
    currency = models.CharField(max_length=3)
    contract_size = models.FloatField()
    contract_units = models.CharField(max_length=20)
    tick_size = models.FloatField() # In contract units 
    min_price_fluctuation = models.FloatField() # Tick Size * Contract Size = $12.50
    continuous = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # last_trading_day = models.TextField() # Example: Trading terminates on the business day prior to the 15th day of the contract month
    # trading_hours = models.TextField()  # This can be a text field as the information is quite detailed
    # contract_months = models.CharField(max_length=100) # months that exists for the procude



    def __str__(self):
        return f"Future(asset={self.asset}, expiration_date={self.expiration_date})"
    
class Cryptocurrency(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='cryptocurrency')
    cryptocurrency_name = models.CharField(max_length=50)
    circulating_supply = models.IntegerField(null=True, blank=True)
    market_cap = models.IntegerField(null=True, blank=True)
    total_supply = models.IntegerField(null=True, blank=True)
    max_supply = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cryptocurrency(name={self.cryptocurrency_name})"
    
class Option(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='option')
    strike_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateTimeField()
    option_type = models.CharField(max_length=4)  # 'CALL' or 'PUT'
    contract_size = models.IntegerField()
    underlying_name = models.CharField(max_length=50)
    exchange = models.CharField(max_length=25, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # Other specific fields for options

    def __str__(self):
        return f"Option(asset={self.asset}, strike_price={self.strike_price}, type={self.option_type})"
