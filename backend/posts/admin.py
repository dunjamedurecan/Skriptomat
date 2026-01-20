from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'course', 'status', 'uploaded_at', 'total_likes')
    list_filter = ('status', 'course__faculty', 'uploaded_at')
    search_fields = ('title', 'post', 'user__username', 'user__email')
    readonly_fields = ('uploaded_at', 'reviewed_at', 'total_likes')
    
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'post', 'user', 'course')
        }),
        ('Document', {
            'fields': ('file',)
        }),
        ('Moderation', {
            'fields': ('status', 'reviewed_by', 'reviewed_at')
        }),
        ('Engagement', {
            'fields': ('uploaded_at', 'total_likes')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'course', 'course__faculty', 'reviewed_by')
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
