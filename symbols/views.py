from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Symbol, Equity, Cryptocurrency, Option, Future, Index, AssetClass, Currency
from .serializers import SymbolReadSerializer, SymbolWriteSerializer, EquitySerializer,  CryptocurrencySerializer, FutureSerializer, OptionSerializer, AssetClassSerializer, CurrencySerializer, IndexSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import APIException
import logging

logger = logging.getLogger(__name__)

class AssetClassViewSet(viewsets.ModelViewSet):
    queryset = AssetClass.objects.all()
    serializer_class = AssetClassSerializer

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class SymbolViewSet(viewsets.ModelViewSet):
    queryset = Symbol.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return SymbolReadSerializer
        return SymbolWriteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        ticker = self.request.query_params.get('ticker')
        try:
            if ticker:
                # Correctly use the `ticker` field for filtering
                return queryset.filter(ticker__iexact=ticker)
            return queryset
        except Exception as e:
            # Log the exception for debugging
            logger.error(f"Error in get_queryset: {str(e)}")
            # Return a generic server error response
            raise APIException(detail="An error occurred while retrieving symbols.", code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        raise PermissionDenied(detail="Direct creation of Symbol is not allowed.")

    def perform_update(self, serializer):
        raise PermissionDenied(detail="Direct updating of Symbol is not allowed.")

class IndexViewSet(viewsets.ModelViewSet):
    queryset = Index.objects.all()
    serializer_class = IndexSerializer

    # This method is called when saving a new object instance.
    # You can add custom creation logic here if needed.
    def perform_create(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            # Log the exception for debugging
            logger.error(f"Error in perform_create: {str(e)}")
            # Raise an APIException with a custom message
            raise APIException("Failed to create benchmark. Please check your data.")

    def perform_update(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            logger.error(f"Error in perform_update: {str(e)}")
            # Raise an APIException with a custom message
            raise APIException("Failed to update benchmark. Please check your data.")

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


