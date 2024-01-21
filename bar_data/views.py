from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from django.db import IntegrityError
from .models import BarData
from .serializers import BarDataSerializer
from assets.models import Asset
import datetime

class BarDataViewSet(viewsets.ModelViewSet):
    queryset = BarData.objects.all()
    serializer_class = BarDataSerializer

    @action(methods=['post'], detail=False)
    def bulk_create(self, request, *args, **kwargs):
        equity_data_list = request.data

        if not isinstance(equity_data_list, list):
            return Response({'error': 'Input data should be a list'}, status=status.HTTP_400_BAD_REQUEST)

        created_or_updated_objects = []
        errors = []

        for equity_data in equity_data_list:
            try:
                with transaction.atomic():
                    symbol = equity_data.get('symbol')
                    if not symbol:
                        errors.append({'error': 'Symbol is required for each item'})
                        continue

                    asset = Asset.objects.get(symbol=symbol)
                    defaults = equity_data.copy()
                    defaults.pop('symbol', None)  # Remove non-model fields if necessary

                    obj, created = BarData.objects.update_or_create(
                        asset=asset, 
                        timestamp=equity_data.get('timestamp'), 
                        defaults=defaults
                    )
                    created_or_updated_objects.append(obj)

            except IntegrityError as e:
                errors.append({'error': str(e)})
                continue
            except Exception as e:
                errors.append({'error': str(e)})
                continue

        return Response({
            'created_or_updated': self.get_serializer(created_or_updated_objects, many=True).data,
            'errors': errors
        }, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = super().get_queryset()
        symbols = self.request.query_params.get('symbols')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if symbols:
            symbol_list = symbols.split(',')
            assets = Asset.objects.filter(symbol__in=symbol_list)
            queryset = queryset.filter(asset__in=assets)

        if start_date:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            queryset = queryset.filter(timestamp__gte=start_date)

        if end_date:
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            queryset = queryset.filter(timestamp__lte=end_date)

        return queryset

