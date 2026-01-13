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

    def get_serializer_context(self):
       context=super().get_serializer_context()
       context['request']=self.request
       return context

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
        user = self.request.user
    
        if user.role and user.role.name.lower() == 'moderator':
            queryset = Document.objects.filter(status=Document.Status.PENDING)
        
        # Filtriranje po fakultetu moderatora
            if user.faculty:
                queryset = queryset.filter(course__faculty=user.faculty)
            return queryset.order_by("-uploaded_at")
        queryset = Document.objects.filter(status=Document.Status.APPROVED)
        return queryset.order_by("-uploaded_at")
    
    @action(detail=True, methods=['post'])
    def approve(self,request,pk=None):
        document=self.get_object()
        if request.user.role.name.lower()!='moderator':
            return Response({'detail':'Only moderators can approve documents.'},status=403)
        document.status=Document.Status.APPROVED
        document.save()
        return Response({'detail':'Document approved.'})
    
    @action(detail=True, methods=['post'])
    def reject(self,request,pk=None):
        document=self.get_object()
        if request.user.role.name.lower()!='moderator':
            return Response({'detail':'Only moderators can reject documents.'},status=403)
        document.status=Document.Status.REJECTED
        document.save()
        return Response({'detail':'Document rejected.'})