from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Course
from .serializers import InstructorCourseSerializer
from .permissions import IsInstructor, IsCourseOwner


class InstructorCourseListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = InstructorCourseSerializer
    permission_classes = [IsInstructor]

    def get_queryset(self):
        return Course.objects.filter(
            instructor__user=self.request.user
        )

    def perform_create(self, serializer):
        instructor = self.request.user.instructor_profile

        if not instructor.is_verified:
            raise PermissionDenied("Instructor is not verified.")

        serializer.save(instructor=instructor)


class InstructorCourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InstructorCourseSerializer
    permission_classes = [IsInstructor, IsCourseOwner]

    def get_queryset(self):
        return Course.objects.filter(
            instructor__user=self.request.user
        )



class CoursePublishAPIView(APIView):
    permission_classes = [IsInstructor]

    def post(self, request, pk):
        course = get_object_or_404(
            Course,
            pk=pk,
            instructor__user=request.user
        )

        if not course.title or not course.description:
            raise PermissionDenied(
                "Course must have title and description."
            )

        course.is_published = True
        course.save()

        return Response(
            {"detail": "Course published."},
            status=status.HTTP_200_OK
        )
    
class PublicCourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.filter(is_published=True)
    serializer_class = InstructorCourseSerializer
