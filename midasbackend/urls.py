from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from assets.views import AssetViewSet, EquityViewSet, CryptocurrencyViewSet, FutureViewSet, OptionViewSet
from bar_data.views import BarDataViewSet

# router = DefaultRouter()
# router.register(r'assets', AssetViewSet)
# router.register(r'equities', EquityViewSet)
# # router.register(r'commodities', CommodityViewSet)
# router.register(r'cryptocurrencies', CryptocurrencyViewSet)
# router.register(r'futures', FutureViewSet)
# router.register(r'options', OptionViewSet)
# router.register(r'bardata', BarDataViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include([
        path("", include('bar_data.urls')),
        path("", include('backtest.urls')),
        path("", include('account.urls')),
        path("", include('assets.urls')),
    ])),
]