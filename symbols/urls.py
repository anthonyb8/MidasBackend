# assets/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (SymbolViewSet, EquityViewSet, CurrencyViewSet, AssetClassViewSet, SecurityTypeViewSet, IndustryViewSet,
                    ContractUnitsViewSet, VenueViewSet, FutureViewSet, IndexViewSet)

router = DefaultRouter()
router.register(r'venue', VenueViewSet)
router.register(r'currency', CurrencyViewSet)
router.register(r'industry', IndustryViewSet)
router.register(r'asset_class', AssetClassViewSet)
router.register(r'security_type', SecurityTypeViewSet)
router.register(r'contract_units', ContractUnitsViewSet)
router.register(r'symbols', SymbolViewSet)
router.register(r'equities', EquityViewSet)
router.register(r'futures', FutureViewSet)
router.register(r'indexes', IndexViewSet)
# router.register(r'cryptocurrencies', CryptocurrencyViewSet)
# router.register(r'options', OptionViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
