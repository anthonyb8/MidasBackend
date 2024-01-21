# Generated by Django 5.0.1 on 2024-01-21 18:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Backtest",
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
                ("strategy_name", models.CharField(max_length=255)),
                ("symbols", models.JSONField(default=list)),
                ("start_date", models.CharField(blank=True, max_length=25, null=True)),
                ("end_date", models.DateTimeField(blank=True, null=True)),
                ("capital", models.FloatField(blank=True, null=True)),
                ("strategy_allocation", models.FloatField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="EquityData",
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
                ("timestamp", models.DateTimeField()),
                (
                    "equity_value",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
                ),
                (
                    "percent_drawdown",
                    models.DecimalField(decimal_places=6, default=0.0, max_digits=15),
                ),
                (
                    "percent_return",
                    models.DecimalField(decimal_places=6, default=0.0, max_digits=15),
                ),
                (
                    "backtest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="equity_data",
                        to="backtest.backtest",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PriceData",
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
                ("symbol", models.CharField(max_length=10)),
                ("timestamp", models.DateTimeField()),
                ("open", models.DecimalField(decimal_places=4, max_digits=10)),
                ("close", models.DecimalField(decimal_places=4, max_digits=10)),
                ("high", models.DecimalField(decimal_places=4, max_digits=10)),
                ("low", models.DecimalField(decimal_places=4, max_digits=10)),
                ("volume", models.BigIntegerField()),
                (
                    "backtest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="price_data",
                        to="backtest.backtest",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Signal",
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
                ("timestamp", models.DateTimeField()),
                (
                    "backtest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="signals",
                        to="backtest.backtest",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SummaryStats",
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
                ("total_return", models.FloatField(null=True)),
                ("total_trades", models.IntegerField(null=True)),
                ("total_fees", models.FloatField(null=True)),
                ("net_profit", models.FloatField(null=True)),
                ("ending_equity", models.FloatField(null=True)),
                ("max_drawdown", models.FloatField(null=True)),
                ("avg_win_percent", models.FloatField(null=True)),
                ("avg_loss_percent", models.FloatField(null=True)),
                ("sortino_ratio", models.FloatField(null=True)),
                ("alpha", models.FloatField(null=True)),
                ("beta", models.FloatField(null=True)),
                ("annual_standard_deviation", models.FloatField(null=True)),
                ("profit_and_loss_ratio", models.FloatField(null=True)),
                ("profit_factor", models.FloatField(null=True)),
                (
                    "backtest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="summary_stats",
                        to="backtest.backtest",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Trade",
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
                ("trade_id", models.CharField(max_length=100)),
                ("leg_id", models.CharField(max_length=100)),
                ("timestamp", models.DateTimeField()),
                ("symbol", models.CharField(max_length=50)),
                ("quantity", models.IntegerField()),
                ("price", models.DecimalField(decimal_places=4, max_digits=10)),
                ("cost", models.DecimalField(decimal_places=4, max_digits=10)),
                ("direction", models.CharField(max_length=10)),
                (
                    "backtest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trades",
                        to="backtest.backtest",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TradeInstruction",
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
                ("ticker", models.CharField(max_length=100)),
                ("direction", models.CharField(max_length=10)),
                ("trade_id", models.PositiveIntegerField()),
                ("leg_id", models.PositiveIntegerField()),
                ("allocation_percent", models.FloatField()),
                (
                    "signal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trade_instructions",
                        to="backtest.signal",
                    ),
                ),
            ],
        ),
    ]
