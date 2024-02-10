from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from django.db import IntegrityError
from .models import BarData
from .serializers import BarDataSerializer
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

from symbols.models import Symbol
import datetime


from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import BarData
from .serializers import BarDataSerializer

class BarDataViewSet(viewsets.ModelViewSet):
    queryset = BarData.objects.all()
    serializer_class = BarDataSerializer

    @action(methods=['post'], detail=False)
    def bulk_create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)  # Note 'many=True' for bulk operations
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = super().get_queryset()
        tickers = self.request.query_params.get('tickers')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if tickers:
            ticker_list = tickers.split(',')
            queryset = queryset.filter(symbol__ticker__in=ticker_list)  # Adjusted to filter by symbol's ticker

        if start_date and end_date:
            # Assuming start_date and end_date are both provided and correctly formatted
            queryset = queryset.filter(timestamp__range=[start_date, end_date])

        return queryset


# class BarDataViewSet(viewsets.ModelViewSet):
#     queryset = BarData.objects.all()
#     serializer_class = BarDataSerializer

#     @action(methods=['post'], detail=False)
#     def bulk_create(self, request, *args, **kwargs):
#         data_list = request.data

#         if not isinstance(data_list, list):
#             return Response({'error': 'Input data should be a list'}, status=status.HTTP_400_BAD_REQUEST)

#         created_or_updated_objects = []
#         errors = []

#         for bar in data_list:
#             try:
#                 with transaction.atomic():
#                     ticker = bar.get('ticker')
#                     if not ticker:
#                         errors.append({'error': 'Ticker is required for each item'})
#                         continue

#                     symbol_obj = Symbol.objects.get(ticker=ticker)
#                     defaults = bar.copy()
#                     defaults.pop('ticker', None)  # Remove ticker from defaults

#                     # Parse the timestamp if it's provided
#                     timestamp_str = bar.get('timestamp')
#                     if timestamp_str:
#                         timestamp = parse_datetime(timestamp_str)
#                         # No need to make it aware if it's already aware
#                         defaults['timestamp'] = timestamp

#                     obj, created = BarData.objects.update_or_create(
#                         ticker=symbol_obj, 
#                         timestamp=defaults.pop('timestamp'),  # Extract timestamp from defaults
#                         defaults=defaults
#                     )
#                     created_or_updated_objects.append(obj)

#             except IntegrityError as e:
#                 errors.append({'error': str(e)})
#                 continue
#             except Symbol.DoesNotExist:
#                 errors.append({'error': f"Symbol with ticker {ticker} does not exist"})
#                 continue
#             except Exception as e:
#                 errors.append({'error': str(e)})
#                 continue

#         return Response({
#             'created_or_updated': self.get_serializer(created_or_updated_objects, many=True).data,
#             'errors': errors
#         }, status=status.HTTP_201_CREATED)

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         tickers = self.request.query_params.get('tickers')
#         start_date = self.request.query_params.get('start_date')
#         end_date = self.request.query_params.get('end_date')

#         if tickers:
#             ticker_list = tickers.split(',')
#             tickers = Symbol.objects.filter(ticker__in=ticker_list)  # Adjusted to 'ticker'
#             queryset = queryset.filter(ticker__in=tickers)

#         if start_date:
#             start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
#             queryset = queryset.filter(timestamp__gte=start_date)

#         if end_date:
#             end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
#             queryset = queryset.filter(timestamp__lte=end_date)

#         return queryset
    



# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from django.db import transaction
# from django.db import IntegrityError
# from .models import BarData
# from .serializers import BarDataSerializer
# from symbols.models import Symbol
# import datetime

# class BarDataViewSet(viewsets.ModelViewSet):
#     queryset = BarData.objects.all()
#     serializer_class = BarDataSerializer

#     @action(methods=['post'], detail=False)
#     def bulk_create(self, request, *args, **kwargs):
#         equity_data_list = request.data

#         if not isinstance(equity_data_list, list):
#             return Response({'error': 'Input data should be a list'}, status=status.HTTP_400_BAD_REQUEST)

#         created_or_updated_objects = []
#         errors = []

#         for equity_data in equity_data_list:
#             try:
#                 with transaction.atomic():
#                     symbol = equity_data.get('symbol')
#                     if not symbol:
#                         errors.append({'error': 'Symbol is required for each item'})
#                         continue

#                     symbol = Symbol.objects.get(symbol=symbol)
#                     defaults = equity_data.copy()
#                     defaults.pop('symbol', None)  # Remove non-model fields if necessary

#                     obj, created = BarData.objects.update_or_create(
#                         symbol=symbol, 
#                         timestamp=equity_data.get('timestamp'), 
#                         defaults=defaults
#                     )
#                     created_or_updated_objects.append(obj)

#             except IntegrityError as e:
#                 errors.append({'error': str(e)})
#                 continue
#             except Exception as e:
#                 errors.append({'error': str(e)})
#                 continue

#         return Response({
#             'created_or_updated': self.get_serializer(created_or_updated_objects, many=True).data,
#             'errors': errors
#         }, status=status.HTTP_201_CREATED)

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         symbols = self.request.query_params.get('symbols')
#         start_date = self.request.query_params.get('start_date')
#         end_date = self.request.query_params.get('end_date')

#         if symbols:
#             symbol_list = symbols.split(',')
#             symbols = Symbol.objects.filter(symbol__in=symbol_list)
#             queryset = queryset.filter(symbol__in=symbols)

#         if start_date:
#             start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
#             queryset = queryset.filter(timestamp__gte=start_date)

#         if end_date:
#             end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
#             queryset = queryset.filter(timestamp__lte=end_date)

#         return queryset

