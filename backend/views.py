from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from backend.models import Document
from backend.serializers import DocumentSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset=Document.objects.all().order_by("-uploaded_at")
    serializer_class=DocumentSerializer
    permission_classes=[permissions.AllowAny]
    parser_classes=[MultiPartParser,FormParser]