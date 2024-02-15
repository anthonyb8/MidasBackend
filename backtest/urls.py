from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (BacktestViewSet, StaticStatsViewSet, TimeseriesStatsViewSet, TradeViewSet, SignalViewSet)

router = DefaultRouter()
router.register(r'backtest', BacktestViewSet)
router.register(r'staic_stats', StaticStatsViewSet)
router.register(r'timeseries_stats', TimeseriesStatsViewSet)
router.register(r'trades', TradeViewSet)
router.register(r'signals', SignalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
