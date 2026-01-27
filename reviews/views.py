from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count
from .models import Review
from .serializers import ReviewSerializer
from .utils import update_course_rating
from enrollments.models import Enrollment
from courses.models import Course
from enrollments.permissions import IsStudent


class ReviewCreateAPIView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsStudent]

    def perform_create(self, serializer):
        course = get_object_or_404(
            Course,
            pk=self.kwargs["course_id"],
            is_published=True
        )

        if course.instructor.user == self.request.user:
            raise PermissionDenied(
                "Instructor cannot review own course."
            )

        is_enrolled = Enrollment.objects.filter(
            student=self.request.user,
            course=course
        ).exists()

        if not is_enrolled:
            raise PermissionDenied(
                "You must be enrolled to review this course."
            )

        serializer.save(
            student=self.request.user,
            course=course
        )
    
        update_course_rating(course)


class CourseReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(
            course_id=self.kwargs["course_id"]
        )
