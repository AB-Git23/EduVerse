from rest_framework import serializers
from .models import Lesson, LessonProgress


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "section",
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


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ["is_completed", "completed_at"]
        read_only_fields = ["completed_at"]

