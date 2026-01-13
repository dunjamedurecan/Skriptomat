from django.db import models
from django.core.exceptions import ValidationError
from backend import settings
from users.models import Course

def validate_pdf(file):
    if file.content_type != "application/pdf":
        raise ValidationError("Only PDF files are allowed.")
    max_size = 5 * 1024 * 1024  # 5 MB limit
    if file.size > max_size:
        raise ValidationError("File too large (max 5 MB).")

class Document(models.Model):
    class Status(models.TextChoices):
        PENDING='pending','Pending',
        APPROVED='approved','Approved',
        REJECTED='rejected','Rejected',
    
    post = models.CharField(max_length=200,blank=True)
    title = models.CharField(max_length=200, blank=True)
    file = models.FileField(upload_to="pdfs/", validators=[validate_pdf])
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

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title or f"Document {self.pk}"