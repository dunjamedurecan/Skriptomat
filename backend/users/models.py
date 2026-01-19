from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    STUDENT='student'
    MODERATOR='moderator'
    ADMIN='admin'

    ROLE_CHOICES=[
        (STUDENT,'Student'),
        (MODERATOR,'Moderator'),
        (ADMIN,'Admin'),
    ]
    """User roles (Student, Admin, etc.)"""
    name = models.CharField(unique=True, choices=ROLE_CHOICES,max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'roles'

class Faculty(models.Model):
   
    name=models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'faculties'

class Course(models.Model):
    name=models.CharField(max_length=255)
    faculty=models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    semester=models.IntegerField()
    def __str__(self):
        return f"{self.name} ({self.faculty.name}, Semestar {self.semester})"
    class Meta:
        db_table = 'courses'
        unique_together = [['faculty', 'name']]

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

    faculty=models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    
    # PayPal email for receiving donations (Buy Me a Coffee feature)
    # Users who set this can receive tips on their posts
    paypal_email = models.EmailField(
        blank=True,
        null=True,
        help_text="PayPal email for receiving donations. Leave blank to disable tips on your posts."
    )
    
    # Course subscriptions - users can subscribe to courses from their faculty
    subscribed_courses = models.ManyToManyField(
        Course,
        blank=True,
        related_name='subscribers',
        help_text="Courses the user is subscribed to. Only courses from user's faculty."
    )
    
    # Login with email instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Required when creating superuser
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.email
    
    def is_student(self):
        return self.role and self.role.name.lower()=='student'
    
    def is_moderator(self):
        return self.role and self.role.name.lower()=='moderator'
    
    def is_admin(self):
        return self.role and self.role.name.lower()=='admin'
    
    def get_username(self):
        return self.username

