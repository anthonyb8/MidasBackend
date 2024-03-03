import logging
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import CustomUser
from .serializers import CustomUserSerializer

logger = logging.getLogger()

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]  # This line allows unauthenticated access
    
    def post(self, request):
        logger.info("Attempting user registration.")
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # Create a user instance but don't save it yet
                user = CustomUser(**serializer.validated_data)

                # Extract password and hash it
                password = request.data.get('password')
                user.password = make_password(password)

                # Now save the user to the database
                user.save()

                # Create a token for the new user
                token, created = Token.objects.get_or_create(user=user)

                logger.info("User registration successful.")
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            
            except Exception as e:
                logger.error(f"User registration failed: {str(e)}")
                return Response({'error': 'User registration failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        logger.error("User registration validation failed.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
class LoginView(APIView):
    permission_classes = [AllowAny]  # This line allows unauthenticated access
    
    def post(self, request, format=None):
        logger.info("Attempting user login.")
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            logger.info(f"User login successful for : {username}")
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            logger.error("Invalid login credentials.")
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Delete the token to log the user out
            request.user.auth_token.delete()
            logger.info("User logged out successfully.")
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Logout failed: {str(e)}")
            return Response({'error': 'Logout failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)