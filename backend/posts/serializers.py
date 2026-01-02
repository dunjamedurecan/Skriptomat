from rest_framework import serializers
from posts.models import Document

class DocumentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    total_likes=serializers.IntegerField(read_only=True)
    liked=serializers.SerializerMethodField()

    class Meta:
        model=Document
        fields=["id","title","post","file","uploaded_at","user","total_likes","liked"]

    def get_liked(self,obj):
        #provjera je li trenutni korisnik lajkao objavu
        user=self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(id=user.id).exists()
        return False