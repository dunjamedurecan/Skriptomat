from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role, Faculty, Course


class CustomUserAdmin(BaseUserAdmin):
    """Custom User admin that includes faculty field"""
    list_display = ['email', 'username', 'first_name', 'last_name', 'faculty', 'role', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'faculty', 'role']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('faculty', 'role', 'paypal_email')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('faculty', 'role', 'paypal_email')}),
    )


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'faculty', 'semester']
    list_filter = ['faculty', 'semester']
    search_fields = ['name']


admin.site.register(User, CustomUserAdmin)
admin.site.register(Role)