from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Asset, Equity, Cryptocurrency, Option, Future
from .serializers import AssetReadSerializer, AssetWriteSerializer, EquitySerializer,  CryptocurrencySerializer, FutureSerializer, OptionSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import APIException
import logging

logger = logging.getLogger(__name__)


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AssetReadSerializer
        return AssetWriteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        symbol = self.request.query_params.get('symbol')
        try:
            if symbol:
                return queryset.filter(symbol__iexact=symbol.upper())
            return queryset
        except Exception as e:
            # Log the exception for debugging
            logger.error(f"Error in get_queryset: {str(e)}")
            # Return a generic server error response
            raise APIException(detail="An error occurred while retrieving assets.", code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        raise PermissionDenied(detail="Direct creation of Asset is not allowed.")

    def perform_update(self, serializer):
        raise PermissionDenied(detail="Direct updating of Asset is not allowed.")

class EquityViewSet(viewsets.ModelViewSet):
    queryset = Equity.objects.all()
    serializer_class = EquitySerializer

    def perform_create(self, serializer):
        # This method is called when saving a new object instance.
        # You can add custom creation logic here if needed.
        try:
            serializer.save()
        except Exception as e:
            # Log the exception for debugging
            logger.error(f"Error in perform_create: {str(e)}")
            # Raise an APIException with a custom message
            raise APIException("Failed to create equity. Please check your data.")

    def perform_update(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            logger.error(f"Error in perform_update: {str(e)}")
            # Raise an APIException with a custom message
            raise APIException("Failed to update equity. Please check your data.")


class FutureViewSet(viewsets.ModelViewSet):
    queryset = Future.objects.all()
    serializer_class = FutureSerializer

    def perform_create(self, serializer):
        # This method is called when saving a new object instance.
        # You can add custom creation logic here if needed.
        serializer.save()

    def perform_update(self, serializer):
        # Custom update logic, similar to perform_create
        serializer.save()

class CryptocurrencyViewSet(viewsets.ModelViewSet):
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencySerializer

    def perform_create(self, serializer):
        # This method is called when saving a new object instance.
        # You can add custom creation logic here if needed.
        serializer.save()

    def perform_update(self, serializer):
        # Custom update logic, similar to perform_create
        serializer.save()

class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

    def perform_create(self, serializer):
        # This method is called when saving a new object instance.
        # You can add custom creation logic here if needed.
        serializer.save()

    def perform_update(self, serializer):
        # Custom update logic, similar to perform_create
        serializer.save()


