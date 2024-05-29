from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from backtest.models import Backtest

class RegressionAnalysis(models.Model):
    backtest = models.OneToOneField(Backtest, related_name='regression_stats', on_delete=models.CASCADE)
    r_squared = models.DecimalField(max_digits=10, decimal_places=8, validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('1.0'))])
    p_value_alpha = models.DecimalField(max_digits=10, decimal_places=8)
    p_value_beta = models.DecimalField(max_digits=10, decimal_places=8)
    risk_free_rate = models.DecimalField(max_digits=5, decimal_places=4)
    alpha = models.DecimalField(max_digits=15, decimal_places=8)
    beta = models.DecimalField(max_digits=10, decimal_places=8)
    # sharpe_ratio = models.DecimalField(max_digits=10, decimal_places=8)
    # annualized_return = models.DecimalField(max_digits=10, decimal_places=8)
    market_contribution = models.DecimalField(max_digits=10, decimal_places=8)
    idiosyncratic_contribution = models.DecimalField(max_digits=10, decimal_places=8)
    total_contribution = models.DecimalField(max_digits=10, decimal_places=8)
    # annualized_volatility = models.DecimalField(max_digits=10, decimal_places=8)
    market_volatility = models.DecimalField(max_digits=10, decimal_places=8)
    idiosyncratic_volatility = models.DecimalField(max_digits=10, decimal_places=8)
    total_volatility = models.DecimalField(max_digits=10, decimal_places=8)
    portfolio_dollar_beta = models.DecimalField(max_digits=15, decimal_places=8)
    market_hedge_nmv = models.DecimalField(max_digits=15, decimal_places=8) 
