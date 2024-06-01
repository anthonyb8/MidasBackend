# Generated by Django 4.2.7 on 2024-06-01 22:41

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("backtest", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RegressionAnalysis",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("risk_free_rate", models.DecimalField(decimal_places=4, max_digits=5)),
                (
                    "r_squared",
                    models.DecimalField(
                        decimal_places=8,
                        max_digits=10,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.0")),
                            django.core.validators.MaxValueValidator(Decimal("1.0")),
                        ],
                    ),
                ),
                (
                    "adjusted_r_squared",
                    models.DecimalField(
                        decimal_places=8,
                        max_digits=10,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.0")),
                            django.core.validators.MaxValueValidator(Decimal("1.0")),
                        ],
                    ),
                ),
                ("RMSE", models.DecimalField(decimal_places=8, max_digits=10)),
                ("MAE", models.DecimalField(decimal_places=8, max_digits=10)),
                ("f_statistic", models.DecimalField(decimal_places=8, max_digits=10)),
                (
                    "f_statistic_p_value",
                    models.DecimalField(decimal_places=8, max_digits=10),
                ),
                ("durbin_watson", models.DecimalField(decimal_places=8, max_digits=10)),
                ("jarque_bera", models.DecimalField(decimal_places=8, max_digits=10)),
                (
                    "jarque_bera_p_value",
                    models.DecimalField(decimal_places=8, max_digits=10),
                ),
                (
                    "condition_number",
                    models.DecimalField(decimal_places=8, max_digits=10),
                ),
                ("vif", models.JSONField(default=dict)),
                ("alpha", models.DecimalField(decimal_places=8, max_digits=15)),
                ("p_value_alpha", models.DecimalField(decimal_places=8, max_digits=15)),
                ("beta", models.JSONField(default=dict)),
                ("p_value_beta", models.JSONField(default=dict)),
                (
                    "total_contribution",
                    models.DecimalField(decimal_places=8, max_digits=10),
                ),
                (
                    "systematic_contribution",
                    models.DecimalField(decimal_places=8, max_digits=10),
                ),
                (
                    "idiosyncratic_contribution",
                    models.DecimalField(decimal_places=8, max_digits=10),
                ),
                (
                    "total_volatility",
                    models.DecimalField(decimal_places=8, max_digits=10),
                ),
                (
                    "systematic_volatility",
                    models.DecimalField(decimal_places=8, max_digits=10),
                ),
                (
                    "idiosyncratic_volatility",
                    models.DecimalField(decimal_places=8, max_digits=10),
                ),
                ("residuals", models.JSONField(default=list, null=True)),
                (
                    "backtest",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="regression_stats",
                        to="backtest.backtest",
                    ),
                ),
            ],
        ),
    ]
