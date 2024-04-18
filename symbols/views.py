import logging
from rest_framework import viewsets, status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed
from .models import Symbol, Equity, Cryptocurrency, Option, Future, Index, AssetClass, Currency, SecurityType, Industry, ContractUnits, Venue
from .serializers import ( AssetClassSerializer, CurrencySerializer, SecurityTypeSerializer, VenueSerializer, IndustrySerializer, ContractUnitsSerializer, 
                          SymbolSerializer, EquitySerializer, FutureSerializer, OptionSerializer, IndexSerializer, CryptocurrencySerializer)

logger = logging.getLogger(__name__)

class AssetClassViewSet(viewsets.ModelViewSet):
    queryset = AssetClass.objects.all()
    serializer_class = AssetClassSerializer

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class SecurityTypeViewSet(viewsets.ModelViewSet):
    queryset = SecurityType.objects.all()
    serializer_class = SecurityTypeSerializer

class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

class IndustryViewSet(viewsets.ModelViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

class ContractUnitsViewSet(viewsets.ModelViewSet):
    queryset = ContractUnits.objects.all()
    serializer_class = ContractUnitsSerializer

class SymbolViewSet(viewsets.ModelViewSet):
    queryset = Symbol.objects.all()
    serializer_class = SymbolSerializer

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

class EquityViewSet(viewsets.ModelViewSet):
    queryset = Equity.objects.all()
    serializer_class = EquitySerializer

    def create(self, request, *args, **kwargs):
        logger.info("Attempt to directly create a Equity via API.")
        raise MethodNotAllowed(method="POST",detail="Direct creation of Equity is not allowed.")
    
    def update(self, request, *args, **kwargs):
        logger.info("Attempt to directly update a Equity via API.")
        raise MethodNotAllowed(method="PUT", detail="Direct updating of Equity is not allowed.")
    
    def destroy(self, request, *args, **kwargs):
        logger.info("Attempt to directly delete Equity via API.")
        raise MethodNotAllowed(method="DELETE", detail="Direct deleting of Equity is not allowed.")
    
class FutureViewSet(viewsets.ModelViewSet):
    queryset = Future.objects.all()
    serializer_class = FutureSerializer

    def create(self, request, *args, **kwargs):
        logger.warn("Attempt to directly create a Future via API.")
        raise MethodNotAllowed(method="POST", detail="Direct creation of Future is not allowed.")
    
    def update(self, request, *args, **kwargs):
        logger.warn("Attempt to directly update a Future via API.")
        raise MethodNotAllowed(method="PUT", detail="Direct updating of Future is not allowed.")
    
    def destroy(self, request, *args, **kwargs):
        logger.warn("Attempt to directly delete Future via API.")
        raise MethodNotAllowed(method="DELETE", detail="Direct deleting of Future is not allowed.")

class CryptocurrencyViewSet(viewsets.ModelViewSet):
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencySerializer

    def create(self, request, *args, **kwargs):
        logger.warn("Attempt to directly create a Cryptocurrency via API.")
        raise MethodNotAllowed(method="POST", detail="Direct creation of Cryptocurrency is not allowed.")
    
    def update(self, request, *args, **kwargs):
        logger.warn("Attempt to directly update a Cryptocurrency via API.")
        raise MethodNotAllowed(method="PUT", detail="Direct updating of Cryptocurrency is not allowed.")
    
    def destroy(self, request, *args, **kwargs):
        logger.warn("Attempt to directly delete Cryptocurrency via API.")
        raise MethodNotAllowed(method="DELETE", detail="Direct deleting of Cryptocurrency is not allowed.")

class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

    def create(self, request, *args, **kwargs):
        logger.warn("Attempt to directly create a Option via API.")
        raise MethodNotAllowed(method="POST", detail="Direct creation of Option is not allowed.")
    
    def update(self, request, *args, **kwargs):
        logger.warn("Attempt to directly update a Option via API.")
        raise MethodNotAllowed(method="PUT", detail="Direct updating of Option is not allowed.")
    
    def destroy(self, request, *args, **kwargs):
        logger.warn("Attempt to directly delete Option via API.")
        raise MethodNotAllowed(method="DELETE", detail="Direct deleting of Option is not allowed.")

class IndexViewSet(viewsets.ModelViewSet):
    queryset = Index.objects.all()
    serializer_class = IndexSerializer

    def create(self, request, *args, **kwargs):
        logger.warn("Attempt to directly create a Index via API.")
        raise MethodNotAllowed(method="POST", detail="Direct creation of Index is not allowed.")
    
    def update(self, request, *args, **kwargs):
        logger.warn("Attempt to directly update a Index via API.")
        raise MethodNotAllowed(method="PUT", detail="Direct updating of Index is not allowed.")
    
    def destroy(self, request, *args, **kwargs):
        logger.warn("Attempt to directly delete Index via API.")
        raise MethodNotAllowed(method="DELETE", detail="Direct deleting of Index is not allowed.")

