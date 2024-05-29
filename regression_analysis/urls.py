from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegressionAnalysisViewSet
                
router = DefaultRouter()
router.register(r'regression_analysis', RegressionAnalysisViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
