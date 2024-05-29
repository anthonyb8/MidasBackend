from backtest.models import Backtest
from rest_framework import serializers
from .models import RegressionAnalysis

class RegressionAnalysisSerializer(serializers.ModelSerializer):
    backtest = serializers.PrimaryKeyRelatedField(queryset=Backtest.objects.all())

    class Meta:
        model = RegressionAnalysis
        fields = [ 
                    "backtest","r_squared", "p_value_alpha","p_value_beta", "risk_free_rate", "alpha", "beta",
                     "market_contribution", "idiosyncratic_contribution", "total_contribution",
                     "market_volatility", "idiosyncratic_volatility", "total_volatility", 
                    "portfolio_dollar_beta", "market_hedge_nmv"
                ]