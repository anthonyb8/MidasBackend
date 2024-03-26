from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PositionSerializer, OrderSerializer, AccountSerializer
from .models import SESSION_DATA

class UpdatePositionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PositionSerializer(data=request.data)
        if serializer.is_valid():
            # Assuming a unique identifier like 'symbol' for positions
            ticker = serializer.validated_data['ticker']
            SESSION_DATA['positions'][ticker] = serializer.validated_data
            return Response({"message": "Position updated successfully."})
        else:
            return Response(serializer.errors, status=400)

class GetPositionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        positions = list(SESSION_DATA['positions'].values())
        return Response(positions)

class UpdateOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            # Assuming 'order_id' as a unique identifier for orders
            order_id = serializer.validated_data['orderId']
            SESSION_DATA['orders'][order_id] = serializer.validated_data
            return Response({"message": "Order updated successfully."})
        else:
            return Response(serializer.errors, status=400)

class GetOrdersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = list(SESSION_DATA['orders'].values())
        return Response(orders)
    
class UpdateAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            # Assuming 'order_id' as a unique identifier for orders
            SESSION_DATA['account'] = serializer.validated_data
            return Response({"message": "Account updated successfully."})
        else:
            return Response(serializer.errors, status=400)

class GetAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = list(SESSION_DATA['account'].values())
        return Response(orders)
    
class ClearSessionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        SESSION_DATA['positions'] = {}
        SESSION_DATA['orders'] = {}
        SESSION_DATA['account'] = {}
        SESSION_DATA['rick_model'] = {}
        SESSION_DATA['market_data'] = {}

        return Response({"message": "Session data cleared successfully"})