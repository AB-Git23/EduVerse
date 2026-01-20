from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Enrollment
from .serializers import EnrollmentSerializer
from .permissions import IsStudent
from courses.models import Course


class StudentEnrollmentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        course_id = self.request.data.get("course")
        course = get_object_or_404(Course, pk=course_id, is_published=True)

        if course.instructor.user == self.request.user:
            raise PermissionDenied("Instructor cannot enroll in own course.")

        serializer.save(student=self.request.user, course=course)
