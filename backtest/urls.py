from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BacktestViewSet
                
router = DefaultRouter()
router.register(r'backtest', BacktestViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
