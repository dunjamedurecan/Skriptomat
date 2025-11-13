from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer, UserSerializer

from rest_framework.views import APIView
from oauth2_provider.models import Application, AccessToken, RefreshToken
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
from django.utils.timezone import now, timedelta
from django.contrib.auth import authenticate


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    POST /api/users/register/
    
    Accepts: email, username, password, password_confirm
    Returns: User data (without password)
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Anyone can register (no auth needed)
    
    def create(self, request, *args, **kwargs):
        """Handle POST request to create new user"""
        serializer = self.get_serializer(data=request.data)
        
        # Validate data
        if serializer.is_valid():
            # Create user
            user = serializer.save()
            
            # Return success response with user data
            user_data = UserSerializer(user).data
            return Response(
                {
                    "message": "Registration successful! Please login.",
                    "user": user_data
                },
                status=status.HTTP_201_CREATED
            )
        
        # Return validation errors
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
            """Handle POST request to login user"""
            username = request.data.get('username')  # Can be email or username
            password = request.data.get('password')
            
            if not username or not password:
                return Response(
                    {"error": "Username and password are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Authenticate user (uses your custom EmailOrUsernameBackend)
            user = authenticate(username=username, password=password)
            
            if user is None:
                return Response(
                    {"error": "Invalid credentials."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if not user.is_active:
                return Response(
                    {"error": "Account is disabled."},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Get OAuth2 application (the one we'll create in admin)
            try:
                application = Application.objects.get(name="Skriptomat Frontend")
            except Application.DoesNotExist:
                return Response(
                    {"error": "OAuth2 application not configured."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Create access token
            expires = now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
            access_token = AccessToken.objects.create(
                user=user,
                application=application,
                token=generate_token(),
                expires=expires,
                scope='read write'
            )
            
            # Create refresh token
            refresh_token = RefreshToken.objects.create(
                user=user,
                application=application,
                token=generate_token(),
                access_token=access_token
            )
            
            # Return tokens and user data
            user_data = UserSerializer(user).data
            
            return Response({
                'access_token': access_token.token,
                'refresh_token': refresh_token.token,
                'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
                'token_type': 'Bearer',
                'user': user_data
            }, status=status.HTTP_200_OK)
    


class TokenRefreshView(APIView):
    """
    API endpoint to refresh access token using refresh token.
    POST /api/users/token/refresh/
    
    Accepts: refresh_token
    Returns: new access_token, new refresh_token
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Handle POST request to refresh access token"""
        refresh_token_string = request.data.get('refresh_token')
        
        if not refresh_token_string:
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Get refresh token from database
            refresh_token = RefreshToken.objects.get(token=refresh_token_string)
        except RefreshToken.DoesNotExist:
            return Response(
                {"error": "Invalid refresh token."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check if refresh token is still valid (not revoked)
        if refresh_token.revoked:
            return Response(
                {"error": "Refresh token has been revoked."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Get the user and application
        user = refresh_token.user
        application = refresh_token.application
        
        # Revoke old access token
        old_access_token = refresh_token.access_token
        old_access_token.delete()
        
        # Create new access token
        expires = now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        new_access_token = AccessToken.objects.create(
            user=user,
            application=application,
            token=generate_token(),
            expires=expires,
            scope='read write'
        )
        
        # If ROTATE_REFRESH_TOKEN is True, create new refresh token
        if oauth2_settings.ROTATE_REFRESH_TOKEN:
            # Revoke old refresh token
            refresh_token.revoke()
            
            # Create new refresh token
            new_refresh_token = RefreshToken.objects.create(
                user=user,
                application=application,
                token=generate_token(),
                access_token=new_access_token
            )
            
            return Response({
                'access_token': new_access_token.token,
                'refresh_token': new_refresh_token.token,
                'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
                'token_type': 'Bearer',
            }, status=status.HTTP_200_OK)
        else:
            # Reuse same refresh token, update its access_token reference
            refresh_token.access_token = new_access_token
            refresh_token.save()
            
            return Response({
                'access_token': new_access_token.token,
                'refresh_token': refresh_token_string,
                'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
                'token_type': 'Bearer',
            }, status=status.HTTP_200_OK)