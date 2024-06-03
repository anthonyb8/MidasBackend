import logging
from backtest.models import Backtest
from rest_framework import serializers
from .services import create_regression_analysis
from .models import RegressionAnalysis, TimeSeriesData

logger = logging.getLogger()

class TimeSeriesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSeriesData
        fields = ['timestamp', "daily_benchmark_return"]

class RegressionAnalysisSerializer(serializers.ModelSerializer):
    backtest = serializers.PrimaryKeyRelatedField(queryset=Backtest.objects.all())
    timeseries_data = TimeSeriesDataSerializer(many=True)

    class Meta:
        model = RegressionAnalysis
        fields = [ 
                    "backtest", "risk_free_rate", "r_squared", "adjusted_r_squared", "RMSE", "MAE", "f_statistic",
                    "f_statistic_p_value", "durbin_watson", "jarque_bera", "jarque_bera_p_value", "condition_number",
                    "vif", "alpha", "p_value_alpha", "beta", "p_value_beta", "total_contribution", "systematic_contribution",
                    "idiosyncratic_contribution", "total_volatility", "systematic_volatility", "idiosyncratic_volatility", "residuals", 
                    "timeseries_data"
                ]
    
    # POST
    def create(self, validated_data):
        logger.info("Creating a new Regression instance with data: %s", validated_data)
        try:
            backtest_instance = create_regression_analysis(validated_data)
            logger.info(f"Successfully created Regression instance with ID: {backtest_instance.id}")
            return backtest_instance
        except Exception as e:
            logger.exception(f"Failed to create a new Regression instance: {str(e)}")
            raise serializers.ValidationError("Failed to create a new Regression instance")
        


