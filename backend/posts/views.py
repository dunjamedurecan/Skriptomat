from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from posts.models import Document
from posts.serializers import DocumentSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset=Document.objects.all().order_by("-uploaded_at")
    serializer_class=DocumentSerializer
    permission_classes=[permissions.IsAuthenticated]
    parser_classes=[MultiPartParser,FormParser]