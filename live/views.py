import logging
from rest_framework import viewsets
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status

from .models import LiveSession, SummaryStats, Trade, Signal
from .serializers import (LiveSessionSerializer, SummaryStatsSerializer, 
                          TradeSerializer, SignalSerializer, LiveSessionListSerializer)

logger = logging.getLogger()

class LiveSessionViewSet(viewsets.ModelViewSet):
    queryset = LiveSession.objects.all()
    serializer_class = LiveSessionSerializer

    def get_serializer_class(self):
        action = self.action
        logger.info(f"Entering get_serializer_class with action: {action}")
        try:
            if action == 'list':
                logger.info("Handling 'list' action in LiveSessionViewSet.")
                return LiveSessionListSerializer
            else:
                logger.info("Handling other actions in LiveSessionViewSet.")
                return super().get_serializer_class()
        except Exception as e:
            logger.error(f"Error in get_serializer_class: {str(e)}")
            raise
        finally:
            logger.info("Exiting get_serializer_class")
    
    # POST
    def create(self, request, *args, **kwargs):
        logger.info("Attempting to create a LiveSession instance.")
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Failed to create a LiveSession instance: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # GET
    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Attempting to retrieve a LiveSession instance with ID: {kwargs.get('pk')}")
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Failed to retrieve a LiveSession instance: {e}")
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request, *args, **kwargs):
        logger.info(f"Attempting to retrieve list of LiveSession instances.")
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Failed to retrieve a list of LiveSession instances.")
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    # PUT
    def update(self, request, *args, **kwargs):
        logger.info(f"Attempting to update a LiveSession instance with ID: {kwargs.get('pk')}")
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Failed to update a LiveSession instance: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # PATCH
    def partial_update(self, request, *args, **kwargs):
        logger.info(f"Attempting to partially update a LiveSession instance with ID: {kwargs.get('pk')}")
        try:
            return super().partial_update(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Failed to partially update a LiveSession instance: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # DELETE
    def destroy(self, request, *args, **kwargs):
        logger.info(f"Attempting to delete a LiveSession instance with ID: {kwargs.get('pk')}")
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Failed to delete a LiveSession instance: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    