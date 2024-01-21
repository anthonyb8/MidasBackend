from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CustomUserSerializer
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]  # This line allows unauthenticated access
    
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            # Create a user instance but don't save it yet
            user = CustomUser(**serializer.validated_data)

            # Extract password and hash it
            password = request.data.get('password')
            user.password = make_password(password)

            # Now save the user to the database
            user.save()

            # Create a token for the new user
            token, created = Token.objects.get_or_create(user=user)

            # Return the token in the response body for command line tools
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = [AllowAny]  # This line allows unauthenticated access
    
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete the token to log the user out
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)