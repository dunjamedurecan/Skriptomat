from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import Faculty,Role
from .serializers import UserRegistrationSerializer, UserSerializer

from rest_framework.views import APIView
from oauth2_provider.models import Application, AccessToken, RefreshToken
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
from django.utils.timezone import now, timedelta
from django.contrib.auth import authenticate, get_user_model

import os
import requests
import secrets

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
       data = request.data
       role_name = data.get("role")
       if role_name and not Role.objects.filter(name=role_name).exists():
            return Response({"role": ["Role does not exist."]}, status=status.HTTP_400_BAD_REQUEST)
       faculty_name = data.get("faculty")
       if faculty_name and not Faculty.objects.filter(name=faculty_name).exists():
            return Response({"faculty": ["Faculty does not exist."]}, status=status.HTTP_400_BAD_REQUEST)
       print("Podaci iz zahteva:", request.data)
       serializer = self.get_serializer(data=request.data)
       if serializer.is_valid():
            print("Validirani podaci u serializeru:", serializer.validated_data)
            user = serializer.save()
            user_data = UserSerializer(user).data
            return Response(
                {"message": "Registration successful! Please login.", "user": user_data},
                status=status.HTTP_201_CREATED,
            )
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response({"error": "Account is disabled."}, status=status.HTTP_403_FORBIDDEN)

        try:
            application = Application.objects.get(name="Skriptomat Frontend")
        except Application.DoesNotExist:
            return Response({"error": "OAuth2 application not configured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        expires = now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        access_token = AccessToken.objects.create(
            user=user, application=application, token=generate_token(), expires=expires, scope="read write"
        )
        refresh_token = RefreshToken.objects.create(user=user, application=application, token=generate_token(), access_token=access_token)
        user_data = UserSerializer(user).data

        return Response(
            {
                "access_token": access_token.token,
                "refresh_token": refresh_token.token,
                "expires_in": oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
                "token_type": "Bearer",
                "user": user_data,
            },
            status=status.HTTP_200_OK,
        )


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token_string = request.data.get("refresh_token")
        if not refresh_token_string:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh_token = RefreshToken.objects.get(token=refresh_token_string)
        except RefreshToken.DoesNotExist:
            return Response({"error": "Invalid refresh token."}, status=status.HTTP_401_UNAUTHORIZED)

        if refresh_token.revoked:
            return Response({"error": "Refresh token has been revoked."}, status=status.HTTP_401_UNAUTHORIZED)

        user = refresh_token.user
        application = refresh_token.application

        old_access_token = refresh_token.access_token
        if old_access_token:
            old_access_token.delete()

        expires = now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        new_access_token = AccessToken.objects.create(
            user=user, application=application, token=generate_token(), expires=expires, scope="read write"
        )

        if oauth2_settings.ROTATE_REFRESH_TOKEN:
            refresh_token.revoke()
            new_refresh_token = RefreshToken.objects.create(user=user, application=application, token=generate_token(), access_token=new_access_token)
            return Response(
                {
                    "access_token": new_access_token.token,
                    "refresh_token": new_refresh_token.token,
                    "expires_in": oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
                    "token_type": "Bearer",
                },
                status=status.HTTP_200_OK,
            )
        else:
            refresh_token.access_token = new_access_token
            refresh_token.save()
            return Response(
                {
                    "access_token": new_access_token.token,
                    "refresh_token": refresh_token_string,
                    "expires_in": oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
                    "token_type": "Bearer",
                },
                status=status.HTTP_200_OK,
            )


class GoogleLoginView(APIView):
    """
    POST /api/users/google/
    Body: { "id_token": "<google-id-token>" }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        id_token = request.data.get("id_token")
        if not id_token:
            return Response({"error": "id_token is required."}, status=status.HTTP_400_BAD_REQUEST)

        tokeninfo_url = "https://oauth2.googleapis.com/tokeninfo"
        try:
            r = requests.get(tokeninfo_url, params={"id_token": id_token}, timeout=5)
            token_info = r.json()
        except Exception:
            return Response({"error": "Failed to verify id_token with Google."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # tokeninfo returns 'error_description' or 'error' on invalid tokens
        if token_info.get("error_description") or token_info.get("error"):
            return Response({"error": "Invalid id_token."}, status=status.HTTP_401_UNAUTHORIZED)

        # Verify audience (ensure token was issued for our frontend client)
        expected_aud = os.environ.get("GOOGLE_CLIENT_ID")
        if expected_aud and token_info.get("aud") != expected_aud:
            return Response({"error": "Invalid token audience."}, status=status.HTTP_401_UNAUTHORIZED)

        # Optionally verify issuer (iss) as well in production
        # if token_info.get('iss') not in ('accounts.google.com', 'https://accounts.google.com'):
        #     return Response({"error": "Invalid token issuer."}, status=status.HTTP_401_UNAUTHORIZED)

        email = token_info.get("email")
        email_verified = str(token_info.get("email_verified")).lower() in ("true", "1")

        if not email or not email_verified:
            return Response({"error": "Google account email not available or not verified."}, status=status.HTTP_400_BAD_REQUEST)

        # Find existing user or create
        user = User.objects.filter(email__iexact=email).first()
        if not user:
            local_part = email.split("@")[0]
            base_username = local_part[:30]
            username = base_username
            suffix = 0
            while User.objects.filter(username__iexact=username).exists():
                suffix += 1
                username = f"{base_username[:28]}{suffix}"
            random_password = secrets.token_urlsafe(16)
            user = User.objects.create_user(username=username, email=email, password=random_password)
            user.save()

        if not user.is_active:
            return Response({"error": "Account is disabled."}, status=status.HTTP_403_FORBIDDEN)

        try:
            application = Application.objects.get(name="Skriptomat Frontend")
        except Application.DoesNotExist:
            return Response({"error": "OAuth2 application not configured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        expires = now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        access_token = AccessToken.objects.create(user=user, application=application, token=generate_token(), expires=expires, scope="read write")
        refresh_token = RefreshToken.objects.create(user=user, application=application, token=generate_token(), access_token=access_token)

        user_data = UserSerializer(user).data

        return Response(
            {
                "access_token": access_token.token,
                "refresh_token": refresh_token.token,
                "expires_in": oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
                "token_type": "Bearer",
                "user": user_data,
            },
            status=status.HTTP_200_OK,
        )
class GoogleRegisterView(APIView):
    """
    Google Registration View
    Koristeći Google id_token potvrđujemo korisnika i zahtevamo popunjavanje dodatnih koraka pre kreiranja.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        id_token = request.data.get("id_token")
        if not id_token:
            return Response({"error": "Google id_token is required."}, status=status.HTTP_400_BAD_REQUEST)

        tokeninfo_url = "https://oauth2.googleapis.com/tokeninfo"
        try:
            r = requests.get(tokeninfo_url, params={"id_token": id_token}, timeout=5)
            token_info = r.json()
        except Exception:
            return Response({"error": "Failed to verify id_token with Google."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Provera grešaka u tokenu
        if token_info.get("error_description") or token_info.get("error"):
            return Response({"error": "Invalid id_token."}, status=status.HTTP_401_UNAUTHORIZED)

        # Proverite da li token odgovara vašoj aplikaciji
        expected_aud = os.environ.get("GOOGLE_CLIENT_ID")
        if expected_aud and token_info.get("aud") != expected_aud:
            return Response({"error": "Invalid token audience."}, status=status.HTTP_401_UNAUTHORIZED)

        # Ekstrahovanje korisničkih informacija
        email = token_info.get("email")
        email_verified = str(token_info.get("email_verified")).lower() in ("true", "1")

        if not email or not email_verified:
            return Response({"error": "Google account email not available or not verified."}, status=status.HTTP_400_BAD_REQUEST)

        # Proverite da li korisnik već postoji
        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            return Response({
                "error": "A user with this email already exists.",
                "step_required": "login"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Prva faza: email potvrđen i vraćamo osnovne podatke
        return Response({
            "email": email,
            "first_name": token_info.get("given_name"),
            "last_name": token_info.get("family_name"),
            "message": "Email confirmed. Proceed with second step to finalize registration."
        }, status=status.HTTP_200_OK)
    
class UserProfileView(APIView):
    permission_classes= [IsAuthenticated]

    def get(self,request,username):
        try:
            user=User.objects.get(username=username)
            print(user)
            serializer=UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error":"User not found."},status=status.HTTP_404_NOT_FOUND)