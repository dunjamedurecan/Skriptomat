from rest_framework import serializers
from posts.models import Document


class DocumentUserSerializer(serializers.Serializer):
    """Serializer for user data within a document (includes paypal_email for donations)"""
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    paypal_email = serializers.EmailField(read_only=True)


class DocumentSerializer(serializers.ModelSerializer):
    # Use nested serializer for user to include paypal_email
    user = DocumentUserSerializer(read_only=True)
    total_likes = serializers.IntegerField(read_only=True)
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ["id", "title", "post", "file", "uploaded_at", "user", "total_likes", "liked"]

    def get_liked(self, obj):
        # Provjera je li trenutni korisnik lajkao objavu
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(id=user.id).exists()
        return False