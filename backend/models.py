from django.db import models
from django.core.exceptions import ValidationError

def validate_pdf(file):
    if file.content_type != "application/pdf":
        raise ValidationError("Only PDF files are allowed.")
    max_size = 5 * 1024 * 1024  # 5 MB limit
    if file.size > max_size:
        raise ValidationError("File too large (max 5 MB).")

class Document(models.Model):
    post=models.CharField(max_length=200,blank=True)
    title = models.CharField(max_length=200, blank=True)
    file = models.FileField(upload_to="pdfs/", validators=[validate_pdf])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Document {self.pk}"