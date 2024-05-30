from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from backtest.models import Backtest

class RegressionAnalysis(models.Model):
    backtest = models.OneToOneField(Backtest, related_name='regression_stats', on_delete=models.CASCADE)
    risk_free_rate = models.DecimalField(max_digits=5, decimal_places=4)
    r_squared = models.DecimalField(max_digits=10, decimal_places=8, validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('1.0'))])
    adjusted_r_squared = models.DecimalField(max_digits=10, decimal_places=8, validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('1.0'))])
    RMSE = models.DecimalField(max_digits=10, decimal_places=8)
    MAE = models.DecimalField(max_digits=10, decimal_places=8)
    RMSE = models.DecimalField(max_digits=10, decimal_places=8)
    MAE = models.DecimalField(max_digits=10, decimal_places=8)
    f_statistic = models.DecimalField(max_digits=10, decimal_places=8)
    f_statistic_p_value = models.DecimalField(max_digits=10, decimal_places=8)
    durbin_watson = models.DecimalField(max_digits=10, decimal_places=8)
    jarque_bera = models.DecimalField(max_digits=10, decimal_places=8)
    jarque_bera_p_value = models.DecimalField(max_digits=10, decimal_places=8)
    condition_number  = models.DecimalField(max_digits=10, decimal_places=8)
    vif = models.JSONField(default=dict)
    alpha = models.DecimalField(max_digits=15, decimal_places=8)
    p_value_alpha = models.DecimalField(max_digits=15, decimal_places=8)
    beta = models.JSONField(default=dict)
    p_value_beta = models.JSONField(default=dict)
    total_contribution = models.DecimalField(max_digits=10, decimal_places=8)
    systematic_contribution = models.DecimalField(max_digits=10, decimal_places=8)
    idiosyncratic_contribution = models.DecimalField(max_digits=10, decimal_places=8)
    total_volatility = models.DecimalField(max_digits=10, decimal_places=8)
    systematic_volatility = models.DecimalField(max_digits=10, decimal_places=8)
    idiosyncratic_volatility = models.DecimalField(max_digits=10, decimal_places=8)
    residuals = models.JSONField(default=list, null=True)
