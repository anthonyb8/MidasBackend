from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BarDataViewSet

router = DefaultRouter()
router.register(r'bardata', BarDataViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
