from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from lessons.models import Lesson
from .models import Course, Section
from .serializers import InstructorCourseSerializer, PublicCourseSerializer
from .permissions import IsInstructor, IsCourseOwner


class InstructorCourseListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = InstructorCourseSerializer
    permission_classes = [IsInstructor]

    def get_queryset(self):
        return Course.objects.filter(instructor__user=self.request.user)

    def perform_create(self, serializer):
        instructor = self.request.user.instructor_profile

        if not instructor.is_verified:
            raise PermissionDenied("Instructor is not verified.")

        serializer.save(instructor=instructor)


class InstructorCourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InstructorCourseSerializer
    permission_classes = [IsInstructor, IsCourseOwner]

    def get_queryset(self):
        return Course.objects.filter(instructor__user=self.request.user)


class CoursePublishAPIView(APIView):
    permission_classes = [IsInstructor]

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk, instructor__user=request.user)

        if not course.title or not course.description:
            raise PermissionDenied("Course must have title and description.")

        has_published_lessons = Lesson.objects.filter(
            section__course=course, is_published=True
        ).exists()

        if not has_published_lessons:
            raise PermissionDenied("Course must have at least one published lesson.")

        course.is_published = True
        course.save()

        return Response({"detail": "Course published."}, status=status.HTTP_200_OK)


class PublicCourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.filter(is_published=True)
    serializer_class = PublicCourseSerializer


class PublicCourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.filter(is_published=True)
    serializer_class = PublicCourseSerializer


class InstructorSectionListCreateAPIView(generics.ListCreateAPIView):
    from .serializers import SectionSerializer
    serializer_class = SectionSerializer
    permission_classes = [IsInstructor]

    def get_queryset(self):
        course_id = self.kwargs["course_id"]
        return Section.objects.filter(course_id=course_id, course__instructor__user=self.request.user)

    def perform_create(self, serializer):
        course_id = self.kwargs["course_id"]
        course = get_object_or_404(Course, pk=course_id, instructor__user=self.request.user)
        
        if course.is_published:
            raise PermissionDenied("Cannot add sections to a published course.")
        
        serializer.save(course=course)


class CourseCompletionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        from enrollments.models import Enrollment
        from lessons.models import LessonProgress
        
        # Verify enrollment
        enrollment = get_object_or_404(Enrollment, student=request.user, course_id=course_id)
        
        # Get all published lessons in the course
        total_lessons = Lesson.objects.filter(
            section__course_id=course_id,
            is_published=True
        ).count()
        
        if total_lessons == 0:
            return Response({"completion_percentage": 0, "completed_lessons": 0, "total_lessons": 0})
        
        # Get completed lessons
        completed_lessons = LessonProgress.objects.filter(
            user=request.user,
            lesson__section__course_id=course_id,
            lesson__is_published=True,
            is_completed=True
        ).count()
        
        completion_percentage = round((completed_lessons / total_lessons) * 100, 2)
        
        return Response({
            "completion_percentage": completion_percentage,
            "completed_lessons": completed_lessons,
            "total_lessons": total_lessons
        })
