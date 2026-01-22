from django.db import models
from django.core.exceptions import ValidationError
from backend import settings
from backend.supabase_storage import SupabaseStorage
from users.models import Course

def validate_pdf(file):
    # Only validate if it's a new upload (not an already-saved file)
    if hasattr(file, 'content_type'):
        if file.content_type != "application/pdf":
            raise ValidationError("Only PDF files are allowed.")
    
    # Check file size (works for both new uploads and saved files)
    max_size = 50 * 1024 * 1024  # 50 MB limit
    if file.size > max_size:
        raise ValidationError("File too large (max 50 MB).")

class Document(models.Model):
    class Status(models.TextChoices):
        PENDING='pending','Pending',
        APPROVED='approved','Approved',
        REJECTED='rejected','Rejected',
    
    post = models.CharField(max_length=200,blank=True)
    title = models.CharField(max_length=200, blank=True)
    file = models.FileField(upload_to="pdfs/", validators=[validate_pdf], storage=SupabaseStorage())
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Koristite AUTH_USER_MODEL
        on_delete=models.CASCADE,
        related_name='documents',
        null=True
    )
    likes=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_documents',blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    course=models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents'
    )
    allow_download=models.BooleanField(default=True)
    reviewed_by=models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='reviewed_documents')
    reviewed_at=models.DateTimeField(null=True,blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title or f"Post {self.pk}"
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'