import logging
from datetime import datetime
from django.db import IntegrityError
from django.utils.dateparse import parse_datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from django.db import transaction

from .models import BarData, QuoteData
from symbols.models import Symbol
from .serializers import BarDataSerializer, QuoteDataSerializer

logger = logging.getLogger(__name__)


class BarDataViewSet(viewsets.ModelViewSet):
    queryset = BarData.objects.all()
    serializer_class = BarDataSerializer

    @action(methods=['post'], detail=False)
    def bulk_create(self, request, *args, **kwargs):
        logger.info("Received request for bulk creation of BarData.")
        if not isinstance(request.data, list):
            logger.error("Input data is not a list.")
            return Response({'error': 'Input data should be a list'}, status=status.HTTP_400_BAD_REQUEST)

        created_objects = []
        errors = []

        with transaction.atomic():
            for index, item_data in enumerate(request.data, start=1):
                serializer = BarDataSerializer(data=item_data)
                if serializer.is_valid():
                    try:
                        obj = serializer.save()
                        created_objects.append(obj)
                    except Exception as e:
                        logger.error(f"Error saving BarData at index {index}: {e}")
                        errors.append({'index': index, 'error': str(e)})
                else:
                    logger.error(f"Validation failed for BarData at index {index}: {serializer.errors}")
                    errors.append({'index': index, 'errors': serializer.errors})
                    
        response_status = status.HTTP_201_CREATED if not errors else status.HTTP_207_MULTI_STATUS

        return Response({
            'created': BarDataSerializer(created_objects, many=True).data,
            'errors': errors
        }, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tickers = self.request.query_params.get('tickers')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if tickers:
            ticker_list = tickers.split(',')
            queryset = queryset.filter(symbol__ticker__in=ticker_list)

        if start_date and end_date:
            queryset = queryset.filter(timestamp__range=[start_date, end_date])

        logger.info("Custom queryset for BarDataViewSet applied.")
        return queryset
    
class QuoteDataViewSet(viewsets.ModelViewSet):
    queryset = QuoteData.objects.all()
    serializer_class = QuoteDataSerializer

    @action(methods=['post'], detail=False)
    def bulk_create(self, request, *args, **kwargs):
        logger.info("Received request for bulk creation of QuoteData.")
        if not isinstance(request.data, list):
            logger.error("Input data is not a list.")
            return Response({'error': 'Input data should be a list'}, status=status.HTTP_400_BAD_REQUEST)

        created_objects = []
        errors = []

        with transaction.atomic():
            for index, item_data in enumerate(request.data, start=1):
                serializer = QuoteDataSerializer(data=item_data)
                if serializer.is_valid():
                    try:
                        obj = serializer.save()
                        created_objects.append(obj)
                    except Exception as e:
                        logger.error(f"Error saving QuoteData at index {index}: {e}")
                        errors.append({'index': index, 'error': str(e)})
                else:
                    logger.error(f"Validation failed for QuoteData at index {index}: {serializer.errors}")
                    errors.append({'index': index, 'errors': serializer.errors})
                    
        response_status = status.HTTP_201_CREATED if not errors else status.HTTP_207_MULTI_STATUS

        return Response({
            'created': QuoteDataSerializer(created_objects, many=True).data,
            'errors': errors
        }, status=status.HTTP_201_CREATED)
    
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tickers = self.request.query_params.get('tickers')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if tickers:
            ticker_list = tickers.split(',')
            queryset = queryset.filter(symbol__ticker__in=ticker_list)

        if start_date and end_date:
            queryset = queryset.filter(timestamp__range=[start_date, end_date])

        logger.info("Custom queryset for QuoteDataViewSet applied.")
        return queryset