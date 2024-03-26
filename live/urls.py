from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LiveSessionViewSet

router = DefaultRouter()
router.register(r'live_session', LiveSessionViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
