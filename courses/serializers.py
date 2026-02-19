from rest_framework import serializers
from .models import Course, Section
from lessons.serializers import StudentLessonSerializer


class SectionSerializer(serializers.ModelSerializer):
    lessons = StudentLessonSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = [
            "id",
            "title",
            "order",
            "lessons",
        ]


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


class PublicCourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(
        source="instructor.user.username", read_only=True
    )
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "instructor_name",
            "average_rating",
            "reviews_count",
            "created_at",
            "sections",
        ]
