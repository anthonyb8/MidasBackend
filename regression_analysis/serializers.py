from backtest.models import Backtest
from rest_framework import serializers
from .models import RegressionAnalysis

class RegressionAnalysisSerializer(serializers.ModelSerializer):
    backtest = serializers.PrimaryKeyRelatedField(queryset=Backtest.objects.all())

    class Meta:
        model = RegressionAnalysis
        fields = [ 
                    "backtest", "risk_free_rate", "r_squared", "adjusted_r_squared", "RMSE", "MAE", "f_statistic",
                    "f_statistic_p_value", "durbin_watson", "jarque_bera", "jarque_bera_p_value", "condition_number",
                    "vif", "alpha", "p_value_alpha", "beta", "p_value_beta", "total_contribution", "systematic_contribution",
                    "idiosyncratic_contribution", "total_volatility", "systematic_volatility", "idiosyncratic_volatility", "residuals"
                ]
        