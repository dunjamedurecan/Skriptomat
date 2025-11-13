from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer, UserSerializer


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
