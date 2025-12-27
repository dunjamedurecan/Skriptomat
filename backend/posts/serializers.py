from rest_framework import serializers
from posts.models import Document

class DocumentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    total_likes=serializers.IntegerField(source='total_likes',read_only=True)
    class Meta:
        model=Document
        fields=["id","title","post","file","uploaded_at","user","total_likes"]