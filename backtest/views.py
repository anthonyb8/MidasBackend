from rest_framework import viewsets
from .models import Backtest, StaticStats, TimeseriesStats, Trade, Signal
from .serializers import (BacktestSerializer, StaticStatsSerializer, TradeSerializer, 
                          TimeseriesStatsSerializer, SignalSerializer, BacktestListSerializer)

class BacktestViewSet(viewsets.ModelViewSet):
    queryset = Backtest.objects.all()
    serializer_class = BacktestSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return BacktestListSerializer
        
        return super().get_serializer_class()
    
class StaticStatsViewSet(viewsets.ModelViewSet):
    queryset = StaticStats.objects.all()
    serializer_class = StaticStatsSerializer

class TimeseriesStatsViewSet(viewsets.ModelViewSet):
    queryset = TimeseriesStats.objects.all()
    serializer_class = TimeseriesStatsSerializer

class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer

class SignalViewSet(viewsets.ModelViewSet):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer


