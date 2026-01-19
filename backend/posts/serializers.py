from rest_framework import serializers
from posts.models import Document
from users.models import Course, User



class DocumentUserSerializer(serializers.Serializer):
    """Serializer for user data within a document (includes paypal_email for donations)"""
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    paypal_email = serializers.EmailField(read_only=True)

class ReviewedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course data"""
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'faculty', 'faculty_name', 'semester']
        read_only_fields = ['id', 'faculty', 'faculty_name']
class DocumentSerializer(serializers.ModelSerializer):
    # Use nested serializer for user to include paypal_email
    user = DocumentUserSerializer(read_only=True)
    total_likes = serializers.IntegerField(read_only=True)
    liked = serializers.SerializerMethodField()
    course = CourseSerializer(read_only=True)
    course_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    semester = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    reviewed_by = ReviewedBySerializer(read_only=True)
    reviewed_at = serializers.DateTimeField(read_only=True)
    allow_download =serializers.BooleanField()

    class Meta:
        model = Document
        fields = ["id", "title", "post", "file", "uploaded_at", "user", "total_likes", "liked","status","course","course_name","semester","reviewed_by","reviewed_at","allow_download"]
        extra_kwargs = {
            'course':{'read_only': True}
        }

    def get_liked(self, obj):
        # Provjera je li trenutni korisnik lajkao objavu
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(id=user.id).exists()
        return False
    
    def validate(self, data):
        course_name=data.get('course_name')
        semester=data.get('semester')
        if course_name and not semester:
            raise serializers.ValidationError("Semester is required when course name is provided.")
        if semester and not course_name:
            raise serializers.ValidationError("Course name is required when semester is provided.")
        return data
    
    def create(self, validated_data):
        course_name=validated_data.pop('course_name',None)
        semester=validated_data.pop('semester',None)
        user=self.context['request'].user

        if not user.faculty:
            raise serializers.ValidationError("User must be associated with a faculty to assign course.")

        if course_name and semester:
            try:
                course=Course.objects.get(
                    name=course_name,
                    faculty=user.faculty)
                if course.semester != semester:
                    raise serializers.ValidationError("Semester does not match the course.")
                validated_data['course'] = course
            except Course.DoesNotExist:
                course=Course.objects.create(
                    name=course_name,
                    faculty=user.faculty,
                    semester=semester
                )
                validated_data['course']=course
        document=Document.objects.create(**validated_data)
        return document
    
    def update(self, instance, validated_data):
        course_name=validated_data.pop('course_name',None)
        semester=validated_data.pop('semester',None)
        user=self.context['request'].user

        if course_name and semester:
            if not user.faculty:
                raise serializers.ValidationError({
                    'faculty': 'Korisnik mora imati dodijeljeni fakultet.'
                })
            try:
                course=Course.objects.get(
                    name=course_name,
                    faculty=user.faculty)
                if course.semester != semester:
                    raise serializers.ValidationError("Semester does not match the course.")
                validated_data['course'] = course
            except Course.DoesNotExist:
                course=Course.objects.create(
                    name=course_name,
                    faculty=user.faculty,
                    semester=semester
                )
                validated_data['course']=course
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
        
