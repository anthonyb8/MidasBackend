from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BarDataViewSet, QuoteDataViewSet

router = DefaultRouter()
router.register(r'bardata', BarDataViewSet)
router.register(r'quotedata', QuoteDataViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
