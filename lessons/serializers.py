from rest_framework import serializers
from .models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "course",
            "title",
            "content",
            "order",
            "is_published",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "is_published",
            "created_at",
        ]

class StudentLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "order",
        ]

