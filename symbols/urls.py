# assets/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SymbolViewSet, EquityViewSet, CryptocurrencyViewSet, FutureViewSet, OptionViewSet, IndexViewSet, CurrencyViewSet, AssetClassViewSet

router = DefaultRouter()
router.register(r'symbols', SymbolViewSet)
router.register(r'equities', EquityViewSet)
router.register(r'cryptocurrencies', CryptocurrencyViewSet)
router.register(r'futures', FutureViewSet)
router.register(r'options', OptionViewSet)
router.register(r'indexes', IndexViewSet)
router.register(r'currency', CurrencyViewSet)
router.register(r'asset_class', AssetClassViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
