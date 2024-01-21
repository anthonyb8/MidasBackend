# assets/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssetViewSet, EquityViewSet, CryptocurrencyViewSet, FutureViewSet, OptionViewSet

router = DefaultRouter()
router.register(r'assets', AssetViewSet)
router.register(r'equities', EquityViewSet)
router.register(r'cryptocurrencies', CryptocurrencyViewSet)
router.register(r'futures', FutureViewSet)
router.register(r'options', OptionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
