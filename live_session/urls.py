from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'sessions', views.SessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('sessions/<int:session_id>/positions/', views.PositionViewSet.as_view({
        'get': 'retrieve_or_list',  # Custom method to decide between list or retrieve
        'post': 'create',
        'put': 'update',      
        'patch': 'partial_update',  
        'delete': 'destroy',  
    }), name='session-positions'),
    path('sessions/<int:session_id>/account/', views.AccountViewSet.as_view({
        'get': 'retrieve_or_list',  # Custom method to decide between list or retrieve
        'post': 'create',
        'put': 'update',      
        'patch': 'partial_update',
        'delete': 'destroy',  
    }), name='session-account'),
    path('sessions/<int:session_id>/orders/', views.OrderViewSet.as_view({
        'get': 'retrieve_or_list',  # Custom method to decide between list or retrieve
        'post': 'create',
        'put': 'update',      
        'patch': 'partial_update',
        'delete': 'destroy',  
    }), name='session-positions'),
    path('sessions/<int:session_id>/risk/', views.RiskViewSet.as_view({
        'get': 'retrieve_or_list',  # Custom method to decide between list or retrieve
        'post': 'create',
        'put': 'update',      
        'patch': 'partial_update',  
        'delete': 'destroy',  
    }), name='session-positions'),
    path('sessions/<int:session_id>/marketdata/', views.MarketDataViewSet.as_view({
        'get': 'retrieve_or_list',  # Custom method to decide between list or retrieve
        'post': 'create',
        'put': 'update',      
        'patch': 'partial_update', 
        'delete': 'destroy',  
    }), name='session-positions'),
]

