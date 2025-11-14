from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    """User roles (Student, Admin, etc.)"""
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'roles'


class User(AbstractUser):
    """Custom User model extending Django's built-in authentication"""
    # Django AbstractUser gives you automatically:
    # - username, email, password (hashed)
    # - first_name, last_name
    # - is_staff, is_active, is_superuser
    # - date_joined, last_login
    
    # Your custom fields:
    role = models.ForeignKey(
        Role, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    
    # Make email required and unique
    email = models.EmailField(unique=True)
    
    # Login with email instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Required when creating superuser
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.email

