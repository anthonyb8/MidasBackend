from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include([
        path("", include('account.urls')),
        path("", include('symbols.urls')),
        path("", include('market_data.urls')),
        path("", include('backtest.urls')),
        path("", include('live.urls')),
        path("", include('live_session.urls')),
        path("", include('regression_analysis.urls')),
    ])),
]