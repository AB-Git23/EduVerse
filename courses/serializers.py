from rest_framework import serializers
from .models import Course


class InstructorCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "is_published",
            "created_at",
        ]
        read_only_fields = ["id", "is_published", "created_at"]


class CoursePublishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["is_published"]

