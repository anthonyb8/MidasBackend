
import logging
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db import IntegrityError
from .models import Session, Position, Account, Order, Risk, MarketData
from .serializers import (PositionSerializer, OrderSerializer, AccountSerializer,
                            RiskSerializer, CreateSessionSerializer, MarketDataSerializer, SessionDetailSerializer)

logger = logging.getLogger(__name__)

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()

    def get_serializer_class(self):
        action = self.action
        logger.info(f"Entering get_serializer_class with action: {action}")
        try:
            if self.action == 'retrieve':
                return SessionDetailSerializer
            else:
                return CreateSessionSerializer
        except Exception as e:
            return Response(f"Error in get_serializer_class: {str(e)}")

    # POST
    def create(self, request, *args, **kwargs):
        logger.info("Attempting to create a Session instance.")
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Failed to create a LiveSession instance: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    # GET
    def retrieve(self, request, *args, **kwargs):
        name = self.kwargs.get('name')
        logger.info(f"Attempting to retrieve a LiveSession instance with name: {name}")
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Failed to retrieve a LiveSession instance: {e}")
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    # DELETE
    def destroy(self, request, *args, **kwargs):
        logger.info(f"Attempting to delete a LiveSession instance with ID: {kwargs.get('pk')}")
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Failed to delete a LiveSession instance: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PositionViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSerializer

    def retrieve_or_list(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        if session_id:
            # Assuming you have logic to determine if this should list or retrieve
            position = get_object_or_404(Position, session__session_id=session_id)
            serializer = self.get_serializer(position)
            return Response(serializer.data)
        else:
            # List logic here if applicable
            pass

    def create(self, request, *args, **kwargs):
        logger.info("Attempting to create a session Position instance.")
        session_id = self.kwargs.get('session_id')
        logger.debug(f"Session ID: {session_id}")

        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Failed to create a session Position instance: {e}", exc_info=True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        session_id = self.kwargs.get('session_id')
        session = get_object_or_404(Session, session_id=session_id)
        try:
            serializer.save(session=session)
            logger.info(f"Position for session ID {session_id} created successfully.")
        except Exception as e:
            logger.error(f"Error saving Position for session ID {session_id}: {e}", exc_info=True)
            raise

    def get_queryset(self):
        session_id = self.kwargs.get('session_id')
        if session_id:
            queryset = Position.objects.filter(session__session_id=session_id)
            logger.debug(f"Queryset for session ID {session_id} retrieved successfully.")
            return queryset
        logger.debug("No session ID provided, returning empty queryset.")
        return Position.objects.none()

    def update(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        logger.info(f"Attempting to update Position for session ID {session_id}.")

        instance = get_object_or_404(Position, session__session_id=session_id)
        serializer = self.get_serializer(instance, data=request.data, partial=(request.method == 'PATCH'))
        
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            logger.info(f"Position for session ID {session_id} updated successfully.")
            return Response(serializer.data)
        else:
            logger.error("Serializer validation failed.", exc_info=True)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            logger.error(f"Failed to perform update: {e}", exc_info=True)
            raise

    def destroy(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        logger.info(f"Attempting to delete Position for session ID {session_id}.")

        try:
            # Retrieve the Position instance associated with the session_id
            instance = get_object_or_404(Position, session__session_id=session_id)
            # Perform the deletion
            instance.delete()
            logger.info(f"Position for session ID {session_id} deleted successfully.")
            # Return a success response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            logger.error(f"Position for session ID {session_id} not found.", exc_info=True)
            return Response({"error": "Position not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Failed to delete Position for session ID {session_id}: {e}", exc_info=True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer

    def retrieve_or_list(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        if session_id:
            # Assuming you have logic to determine if this should list or retrieve
            account = get_object_or_404(Account, session__session_id=session_id)
            serializer = self.get_serializer(account)
            return Response(serializer.data)
        else:
            # List logic here if applicable
            pass

    def create(self, request, *args, **kwargs):
        logger.info("Attempting to create a session Account instance.")
        session_id = self.kwargs.get('session_id')
        logger.debug(f"Session ID: {session_id}")

        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Failed to create a session Account instance: {e}", exc_info=True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        session_id = self.kwargs.get('session_id')
        session = get_object_or_404(Session, session_id=session_id)
        try:
            serializer.save(session=session)
            logger.info(f"Account for session ID {session_id} created successfully.")
        except Exception as e:
            logger.error(f"Error saving Account for session ID {session_id}: {e}", exc_info=True)
            raise

    def get_queryset(self):
        session_id = self.kwargs.get('session_id')
        if session_id:
            queryset = Account.objects.filter(session__session_id=session_id)
            logger.debug(f"Queryset for session ID {session_id} retrieved successfully.")
            return queryset
        logger.debug("No session ID provided, returning empty queryset.")
        return Account.objects.none()

    def update(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        logger.info(f"Attempting to update Account for session ID {session_id}.")

        instance = get_object_or_404(Account, session__session_id=session_id)
        serializer = self.get_serializer(instance, data=request.data, partial=(request.method == 'PATCH'))
        
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            logger.info(f"Account for session ID {session_id} updated successfully.")
            return Response(serializer.data)
        else:
            logger.error("Serializer validation failed.", exc_info=True)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            logger.error(f"Failed to perform update: {e}", exc_info=True)
            raise

    def destroy(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        logger.info(f"Attempting to delete Account for session ID {session_id}.")

        try:
            # Retrieve the Account instance associated with the session_id
            instance = get_object_or_404(Account, session__session_id=session_id)
            # Perform the deletion
            instance.delete()
            logger.info(f"Account for session ID {session_id} deleted successfully.")
            # Return a success response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            logger.error(f"Account for session ID {session_id} not found.", exc_info=True)
            return Response({"error": "Account not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Failed to delete Account for session ID {session_id}: {e}", exc_info=True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def retrieve_or_list(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        if session_id:
            # Assuming you have logic to determine if this should list or retrieve
            order = get_object_or_404(Order, session__session_id=session_id)
            serializer = self.get_serializer(order)
            return Response(serializer.data)
        else:
            # List logic here if applicable
            pass

    def create(self, request, *args, **kwargs):
        logger.info("Attempting to create a session Order instance.")
        session_id = self.kwargs.get('session_id')
        logger.debug(f"Session ID: {session_id}")

        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Failed to create a session Order instance: {e}", exc_info=True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        session_id = self.kwargs.get('session_id')
        session = get_object_or_404(Session, session_id=session_id)
        try:
            serializer.save(session=session)
            logger.info(f"Order for session ID {session_id} created successfully.")
        except Exception as e:
            logger.error(f"Error saving Order for session ID {session_id}: {e}", exc_info=True)
            raise

    def get_queryset(self):
        session_id = self.kwargs.get('session_id')
        if session_id:
            queryset = Order.objects.filter(session__session_id=session_id)
            logger.debug(f"Queryset for session ID {session_id} retrieved successfully.")
            return queryset
        logger.debug("No session ID provided, returning empty queryset.")
        return Order.objects.none()

    def update(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        logger.info(f"Attempting to update Order for session ID {session_id}.")

        instance = get_object_or_404(Order, session__session_id=session_id)
        serializer = self.get_serializer(instance, data=request.data, partial=(request.method == 'PATCH'))
        
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            logger.info(f"Order for session ID {session_id} updated successfully.")
            return Response(serializer.data)
        else:
            logger.error("Serializer validation failed.", exc_info=True)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            logger.error(f"Failed to perform update: {e}", exc_info=True)
            raise

    def destroy(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        logger.info(f"Attempting to delete Order for session ID {session_id}.")

        try:
            # Retrieve the Order instance associated with the session_id
            instance = get_object_or_404(Order, session__session_id=session_id)
            # Perform the deletion
            instance.delete()
            logger.info(f"Order for session ID {session_id} deleted successfully.")
            # Return a success response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            logger.error(f"Order for session ID {session_id} not found.", exc_info=True)
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Failed to delete Order for session ID {session_id}: {e}", exc_info=True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RiskViewSet(viewsets.ModelViewSet):
    serializer_class = RiskSerializer

    def retrieve_or_list(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        if session_id:
            # Assuming you have logic to determine if this should list or retrieve
            risk = get_object_or_404(Risk, session__session_id=session_id)
            serializer = self.get_serializer(risk)
            return Response(serializer.data)
        else:
            # List logic here if applicable
            pass

    def create(self, request, *args, **kwargs):
        logger.info("Attempting to create a session Risk instance.")
        session_id = self.kwargs.get('session_id')
        logger.debug(f"Session ID: {session_id}")

        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Failed to create a session Risk instance: {e}", exc_info=True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        session_id = self.kwargs.get('session_id')
        session = get_object_or_404(Session, session_id=session_id)
        try:
            serializer.save(session=session)
            logger.info(f"Risk for session ID {session_id} created successfully.")
        except Exception as e:
            logger.error(f"Error saving Risk for session ID {session_id}: {e}", exc_info=True)
            raise

    def get_queryset(self):
        session_id = self.kwargs.get('session_id')
        if session_id:
            queryset = Risk.objects.filter(session__session_id=session_id)
            logger.debug(f"Queryset for session ID {session_id} retrieved successfully.")
            return queryset
        logger.debug("No session ID provided, returning empty queryset.")
        return Risk.objects.none()

    def update(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        logger.info(f"Attempting to update Risk for session ID {session_id}.")

        instance = get_object_or_404(Risk, session__session_id=session_id)
        serializer = self.get_serializer(instance, data=request.data, partial=(request.method == 'PATCH'))
        
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            logger.info(f"Risk for session ID {session_id} updated successfully.")
            return Response(serializer.data)
        else:
            logger.error("Serializer validation failed.", exc_info=True)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            logger.error(f"Failed to perform update: {e}", exc_info=True)
            raise

    def destroy(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        logger.info(f"Attempting to delete Risk for session ID {session_id}.")

        try:
            # Retrieve the Risk instance associated with the session_id
            instance = get_object_or_404(Risk, session__session_id=session_id)
            # Perform the deletion
            instance.delete()
            logger.info(f"Risk for session ID {session_id} deleted successfully.")
            # Return a success response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            logger.error(f"Risk for session ID {session_id} not found.", exc_info=True)
            return Response({"error": "Risk not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Failed to delete Risk for session ID {session_id}: {e}", exc_info=True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MarketDataViewSet(viewsets.ModelViewSet):
    serializer_class = MarketDataSerializer

    def retrieve_or_list(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        if session_id:
            # Assuming you have logic to determine if this should list or retrieve
            market_data = get_object_or_404(MarketData, session__session_id=session_id)
            serializer = self.get_serializer(market_data)
            return Response(serializer.data)
        else:
            # List logic here if applicable
            pass

    def create(self, request, *args, **kwargs):
        logger.info("Attempting to create a session MarketData instance.")
        session_id = self.kwargs.get('session_id')
        logger.debug(f"Session ID: {session_id}")

        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Failed to create a session MarketData instance: {e}", exc_info=True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        session_id = self.kwargs.get('session_id')
        session = get_object_or_404(Session, session_id=session_id)
        try:
            serializer.save(session=session)
            logger.info(f"MarketData for session ID {session_id} created successfully.")
        except Exception as e:
            logger.error(f"Error saving MarketData for session ID {session_id}: {e}", exc_info=True)
            raise

    def get_queryset(self):
        session_id = self.kwargs.get('session_id')
        if session_id:
            queryset = MarketData.objects.filter(session__session_id=session_id)
            logger.debug(f"Queryset for session ID {session_id} retrieved successfully.")
            return queryset
        logger.debug("No session ID provided, returning empty queryset.")
        return MarketData.objects.none()

    def update(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        logger.info(f"Attempting to update MarketData for session ID {session_id}.")

        instance = get_object_or_404(MarketData, session__session_id=session_id)
        serializer = self.get_serializer(instance, data=request.data, partial=(request.method == 'PATCH'))
        
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            logger.info(f"MarketData for session ID {session_id} updated successfully.")
            return Response(serializer.data)
        else:
            logger.error("Serializer validation failed.", exc_info=True)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            logger.error(f"Failed to perform update: {e}", exc_info=True)
            raise

    def destroy(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        logger.info(f"Attempting to delete MarketData for session ID {session_id}.")

        try:
            # Retrieve the MarketData instance associated with the session_id
            instance = get_object_or_404(MarketData, session__session_id=session_id)
            # Perform the deletion
            instance.delete()
            logger.info(f"MarketData for session ID {session_id} deleted successfully.")
            # Return a success response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            logger.error(f"MarketData for session ID {session_id} not found.", exc_info=True)
            return Response({"error": "MarketData not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Failed to delete MarketData for session ID {session_id}: {e}", exc_info=True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
