from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from posts.models import Document
from posts.serializers import DocumentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class DocumentViewSet(viewsets.ModelViewSet):
    queryset=Document.objects.all().order_by("-uploaded_at")
    serializer_class=DocumentSerializer
    permission_classes=[permissions.IsAuthenticated]
    parser_classes=[MultiPartParser,FormParser]

    def perform_create(self, serializer):
        # Automatski postavlja prijavljenog korisnika kao vlasnika dokumenta
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        document=self.get_object()
        user=request.user
        if user in document.likes.all(): #ako ga je već lajkao uklanja lajk (like/dislike)
            document.likes.remove(user)
            liked=False
        else:
            document.likes.add(user)
            liked=True
        return Response({'liked': liked, 'total_likes': document.total_likes()})

class PostViewSet(viewsets.ModelViewSet):
    serializer_class=DocumentSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        if user.role and user.role.name.lower()=='moderator':
            return Document.objects.filter(status=Document.Status.PENDING).order_by("-uploaded_at")
        return Document.objects.filter(status=Document.Status.APPROVED)