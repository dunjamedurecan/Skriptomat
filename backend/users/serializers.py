from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Role, Faculty,User

User = get_user_model()  # Gets your custom User model


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Validates email, password, and creates new user account.
    """
    password = serializers.CharField(
        write_only=True,  # Don't return password in response
        min_length=8,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    role=serializers.CharField()  
    faculty=serializers.CharField()
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm', 'first_name', 'last_name','role','faculty']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }
    
    def validate_email(self, value):
        """Check if email already exists"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()  # Store emails in lowercase
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        
        # Check to see that there isn't a user with email equal to registering username
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError("This username is not available.") 
        
        return value
    
    def validate_role(self, value):
        """Ako je role string, traži odgovarajući ID u bazi."""
        if isinstance(value, str):
            role = Role.objects.filter(name=value).first()  # Traži po nazivu
            if not role:
                raise serializers.ValidationError(f"Role '{value}' does not exist.")
            print("Pronađena:",role)
            return role  # Vraćanje ID-a
        return value

    def validate_faculty(self, value):
        """Ako je faculty string, traži odgovarajući ID u bazi."""
        if isinstance(value, str):
            faculty = Faculty.objects.filter(name=value).first()  # Traži po nazivu
            if not faculty:
                raise serializers.ValidationError(f"Faculty '{value}' does not exist.")
            return faculty  # Vraćanje ID-a
        return value
   
    
    def validate(self, data):
        print("Podaci koji su poslati za validaciju:", data)
        if "role" not in data:
            raise serializers.ValidationError({"role": "Role field is required."})

        if "faculty" not in data:
            raise serializers.ValidationError({"faculty": "Faculty field is required."})
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data
    
    def create(self, validated_data):
        """Create and return new user with hashed password"""
        # Remove password_confirm (not needed for User model)
        password = validated_data.pop('password')
        validated_data.pop('password_confirm')
        
        # Create user WITHOUT password first
        user = User(**validated_data)
        # Use set_password to properly hash it
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for returning user data (without password).
    Used for displaying user info in responses.
    """
    role=serializers.StringRelatedField()
    faculty=serializers.StringRelatedField()
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'date_joined', 'role', 'faculty', 'paypal_email']
        read_only_fields = ['id', 'date_joined']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile settings.
    Allows users to update their PayPal email for receiving donations.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'paypal_email']
    
    def validate_paypal_email(self, value):
        """Validate PayPal email format (optional field)"""
        if value and value.strip():
            # Basic email validation is handled by EmailField
            return value.strip().lower()
        return None  # Allow clearing the field


class PublicUserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for public user profile (viewed by other users).
    Shows limited info and whether user accepts donations.
    """
    accepts_donations = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'date_joined', 'accepts_donations', 'paypal_email']
        read_only_fields = fields
    
    def get_accepts_donations(self, obj):
        """Returns True if user has PayPal email set"""
        return bool(obj.paypal_email)
