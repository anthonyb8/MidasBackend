import logging
from django.db import transaction
from django.core.exceptions import ValidationError

from regression_analysis.models import RegressionAnalysis
from .models import RegressionAnalysis, TimeSeriesData

logger = logging.getLogger()


def create_regression_analysis(validated_data):
    try:
        with transaction.atomic():
            logger.info("Starting RegressionAnalysis creation process.")

            # Extract Timeseries Data
            timeseries_stats_data = validated_data.pop('timeseries_data', [])

            # Create the Regression instance
            reg_analysis = RegressionAnalysis.objects.create(**validated_data)
            logger.info(f"RegressionAnalysis instance created with ID: {reg_analysis.id}")

            # Nested object creation for TimeseriesStats
            for data in timeseries_stats_data:
                TimeSeriesData.objects.create(regression_analysis=reg_analysis, **data)
            logger.info("Timeseries stats created.")


            return reg_analysis

    except ValidationError as e:
        logger.error(f"Validation error during regression analysis creation: {e}")
        raise e
    except Exception as e:
        logger.exception(f"Unexpected error during regression analysis creation: {e}")
        raise e