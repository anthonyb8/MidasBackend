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
        logger.info(f"Entering get_serializer_class with action: {self.action}")

        if self.action in ['list', 'retrieve']:
            logger.info("Handling action with SymbolReadSerializer.")
            return SymbolReadSerializer
        else:
            logger.info("Handling action with SymbolWriteSerializer.")
            return SymbolWriteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        ticker = self.request.query_params.get('ticker')
        if ticker:
            try:
                # Filter the queryset based on the 'ticker' query parameter
                queryset = queryset.filter(ticker__iexact=ticker)
            except Exception as e:
                logger.error(f"Error filtering queryset by ticker {ticker}: {str(e)}")
                raise APIException(detail="An error occurred while filtering symbols.", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return queryset
    
    def perform_create(self, serializer):
        logger.warn("Attempt to directly create a Symbol via API.")
        raise PermissionDenied(detail="Direct creation of Symbol is not allowed.")

    def perform_update(self, serializer):
        logger.warn("Attempt to directly update a Symbol via API.")
        raise PermissionDenied(detail="Direct updating of Symbol is not allowed.")

class IndexViewSet(viewsets.ModelViewSet):
    queryset = Index.objects.all()
    serializer_class = IndexSerializer

    def perform_create(self, serializer):
        logger.info("Attempting to save a new Index instance.")
        try:
            serializer.save()
            logger.info("Index instance saved successfully.")
        except Exception as e:
            logger.error(f"Error in perform_create: {str(e)}")
            raise APIException("Failed to create Index. Please check your data.")

    def perform_update(self, serializer):
        logger.info("Attempting to update an Index instance.")
        try:
            serializer.save()
            logger.info("Index instance updated successfully.")
        except Exception as e:
            logger.error(f"Error in perform_update: {str(e)}")
            raise APIException("Failed to update Index. Please check your data.")

class EquityViewSet(viewsets.ModelViewSet):
    queryset = Equity.objects.all()
    serializer_class = EquitySerializer

    def perform_create(self, serializer):
        logger.info("Attempting to save a new Equity instance.")
        try:
            serializer.save()
            logger.info("Equity instance saved successfully.")
        except Exception as e:
            logger.error(f"Error in perform_create: {str(e)}")
            raise APIException("Failed to create Equity. Please check your data.")

    def perform_update(self, serializer):
        logger.info("Attempting to update an Equity instance.")
        try:
            serializer.save()
            logger.info("Equity instance updated successfully.")
        except Exception as e:
            logger.error(f"Error in perform_update: {str(e)}")
            raise APIException("Failed to update Equity. Please check your data.")

class FutureViewSet(viewsets.ModelViewSet):
    queryset = Future.objects.all()
    serializer_class = FutureSerializer

    def perform_create(self, serializer):
        logger.info("Attempting to save a new Future instance.")
        try:
            serializer.save()
            logger.info("Future instance saved successfully.")
        except Exception as e:
            logger.error(f"Error in perform_create: {str(e)}")
            raise APIException("Failed to create Future. Please check your data.")

    def perform_update(self, serializer):
        logger.info("Attempting to update an Future instance.")
        try:
            serializer.save()
            logger.info("Future instance updated successfully.")
        except Exception as e:
            logger.error(f"Error in perform_update: {str(e)}")
            raise APIException("Failed to update Future. Please check your data.")

class CryptocurrencyViewSet(viewsets.ModelViewSet):
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencySerializer

    def perform_create(self, serializer):
        logger.info("Attempting to save a new Cryptocurrency instance.")
        try:
            serializer.save()
            logger.info("Cryptocurrency instance saved successfully.")
        except Exception as e:
            logger.error(f"Error in perform_create: {str(e)}")
            raise APIException("Failed to create Cryptocurrency. Please check your data.")

    def perform_update(self, serializer):
        logger.info("Attempting to update an Cryptocurrency instance.")
        try:
            serializer.save()
            logger.info("Cryptocurrency instance updated successfully.")
        except Exception as e:
            logger.error(f"Error in perform_update: {str(e)}")
            raise APIException("Failed to update Cryptocurrency. Please check your data.")

class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

    def perform_create(self, serializer):
        logger.info("Attempting to save a new Option instance.")
        try:
            serializer.save()
            logger.info("Option instance saved successfully.")
        except Exception as e:
            logger.error(f"Error in perform_create: {str(e)}")
            raise APIException("Failed to create Option. Please check your data.")

    def perform_update(self, serializer):
        logger.info("Attempting to update an Option instance.")
        try:
            serializer.save()
            logger.info("Option instance updated successfully.")
        except Exception as e:
            logger.error(f"Error in perform_update: {str(e)}")
            raise APIException("Failed to update Option. Please check your data.")

