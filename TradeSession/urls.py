from django.urls import path
from .views import UpdatePositionAPIView, GetPositionsAPIView, UpdateAccountAPIView, GetAccountAPIView, UpdateOrderAPIView, GetOrdersAPIView, ClearSessionAPIView

urlpatterns = [
    path('update_positions', UpdatePositionAPIView.as_view(), name='update-positions'),
    path('positions', GetPositionsAPIView.as_view(), name='positions'),
    path('update_orders', UpdateOrderAPIView.as_view(), name='update-orders'),
    path('orders', GetOrdersAPIView.as_view(), name='orders'),
    path('update_account', UpdateAccountAPIView.as_view(), name='update-account'),
    path('account', GetAccountAPIView.as_view(), name='account'),
    path('clear_session', ClearSessionAPIView.as_view(), name='clear-session'),
]   