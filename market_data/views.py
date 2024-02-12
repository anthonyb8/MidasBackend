from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import IntegrityError
from .models import BarData
from .serializers import BarDataSerializer
from django.utils.dateparse import parse_datetime
from rest_framework.exceptions import APIException
from symbols.models import Symbol
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BarDataViewSet(viewsets.ModelViewSet):
    queryset = BarData.objects.all()
    serializer_class = BarDataSerializer

    @action(methods=['post'], detail=False)
    def bulk_create(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            return Response({'error': 'Input data should be a list'}, status=status.HTTP_400_BAD_REQUEST)

        created_objects, errors = self.process_data(request.data)

        if errors:
            # Consider using HTTP_207_MULTI_STATUS for partial success
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            status_code = status.HTTP_201_CREATED

        return Response({
            'created': BarDataSerializer(created_objects, many=True).data,
            'errors': errors
        }, status=status_code)

    def process_data(self, data_list):
        created_objects = []
        errors = []

        for index, bar in enumerate(data_list, start=1):
            ticker = bar.get('symbol')
            timestamp_str = bar.get('timestamp')

            if not ticker or not timestamp_str:
                errors.append(self.error_message(index, 'Symbol and timestamp are required.'))
                continue

            symbol_obj, timestamp, error = self.get_symbol_and_timestamp(ticker, timestamp_str)
            if error:
                errors.append(self.error_message(index, error))
                continue

            obj, error = self.create_or_update_bar_data(symbol_obj, timestamp, bar)
            if error:
                errors.append(self.error_message(index, error))
            else:
                created_objects.append(obj)

        return created_objects, errors

    def get_symbol_and_timestamp(self, ticker, timestamp_str):
        try:
            symbol_obj = Symbol.objects.get(ticker=ticker)
            timestamp = parse_datetime(timestamp_str)
            return symbol_obj, timestamp, None
        except Symbol.DoesNotExist:
            return None, None, f"Symbol with ticker {ticker} does not exist"
        except ValueError:
            return None, None, "Invalid timestamp format."

    def create_or_update_bar_data(self, symbol_obj, timestamp, bar_data):
        defaults = bar_data.copy()
        defaults.pop('symbol', None)
        defaults['timestamp'] = timestamp

        try:
            obj, created = BarData.objects.update_or_create(
                symbol=symbol_obj, timestamp=timestamp, defaults=defaults
            )
            return obj, None
        except IntegrityError as e:
            return None, str(e)

    def error_message(self, index, message):
        return {'index': index, 'error': message}
    
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

        return queryset



