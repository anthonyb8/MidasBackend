from django.db import models

# Asset Details
class AssetClass(models.Model):
    value = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.value

class Currency(models.Model):
    value = models.CharField(max_length=3, unique=True)
    
    def __str__(self):
        return self.value

class SecurityType(models.Model):
    value = models.CharField(max_length=50, unique=True)
   
    def __str__(self):
        return self.value

class ContractUnits(models.Model):
    value = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.value

class Venue(models.Model):
    value = models.CharField(max_length=25, unique=True)
    
    def __str__(self):
        return self.value

class Industry(models.Model):
    value = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.value

#Assets
class Symbol(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    security_type = models.ForeignKey(SecurityType, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.security_type == 'STOCK':
            self.ticker = self.ticker.upper()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('ticker', 'security_type')
    
class Equity(models.Model):
    symbol = models.OneToOneField(Symbol, on_delete=models.CASCADE, related_name='equity')
    company_name = models.CharField(max_length=150)
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, blank=True)
    market_cap = models.FloatField(null=True, blank=True)
    shares_outstanding = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Future(models.Model):
    symbol = models.OneToOneField(Symbol, on_delete=models.CASCADE, related_name='future')
    product_code = models.CharField(max_length=10)  # Example: ZC
    product_name = models.CharField(max_length=50)
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, blank=True)
    contract_size = models.FloatField()
    contract_units = models.ForeignKey(ContractUnits, on_delete=models.SET_NULL, null=True, blank=True)
    tick_size = models.FloatField() # In contract units 
    min_price_fluctuation = models.FloatField() # Tick Size * Contract Size = $12.50
    continuous = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Option(models.Model):
    symbol = models.OneToOneField(Symbol, on_delete=models.CASCADE, related_name='option')
    underlying_name = models.CharField(max_length=50)
    expiration_date = models.DateTimeField()
    strike_price = models.DecimalField(max_digits=10, decimal_places=2)
    contract_size = models.IntegerField()
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=True)
    option_type = models.CharField(max_length=4)  # 'CALL' or 'PUT'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Cryptocurrency(models.Model):
    symbol = models.OneToOneField(Symbol, on_delete=models.CASCADE, related_name='cryptocurrency')
    name = models.CharField(max_length=50)
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    market_cap = models.IntegerField(null=True, blank=True)
    circulating_supply = models.IntegerField(null=True, blank=True)
    total_supply = models.IntegerField(null=True, blank=True)
    max_supply = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Index(models.Model):
    symbol = models.OneToOneField(Symbol, on_delete=models.CASCADE, related_name='index')
    name = models.CharField(max_length=100)  # Increased length for flexibility
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    asset_class = models.ForeignKey(AssetClass, on_delete=models.CASCADE)  # Link to AssetClass model
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=True)
