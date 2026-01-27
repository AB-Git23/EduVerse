from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .serializers import LessonSerializer, StudentLessonSerializer
from .models import Lesson
from courses.models import Course
from enrollments.models import Enrollment
from courses.permissions import IsInstructor


class InstructorLessonListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsInstructor]

    def get_course(self):
        course = get_object_or_404(
            Course, pk=self.kwargs["course_id"], instructor__user=self.request.user
        )
        return course

    def get_queryset(self):
        return Lesson.objects.filter(course=self.get_course())

    def perform_create(self, serializer):
        course = self.get_course()

        if course.is_published is True:
            raise PermissionDenied("Cannot add lessons to a published course.")

        serializer.save(course=course)


class InstructorLessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsInstructor]

    def get_object(self):
        return get_object_or_404(
            Lesson,
            pk=self.kwargs["lesson_id"],
            course__id=self.kwargs["course_id"],
            course__instructor__user=self.request.user,
        )


class LessonPublishAPIView(APIView):
    permission_classes = [IsInstructor]

    def post(self, request, course_id, lesson_id):
        lesson = get_object_or_404(
            Lesson,
            pk=lesson_id,
            course__id=course_id,
            course__instructor__user=request.user,
        )

        if not lesson.title:
            raise PermissionDenied("Lesson must have a title.")

        lesson.is_published = True
        lesson.save()

        return Response({"detail": "Lesson published."}, status=status.HTTP_200_OK)


class StudentLessonListAPIView(generics.ListAPIView):
    serializer_class = StudentLessonSerializer

    def get_queryset(self):
        course_id = self.kwargs["course_id"]

        is_enrolled = Enrollment.objects.filter(
            student=self.request.user,
            course_id=course_id
        ).exists()

        if is_enrolled:
            return Lesson.objects.filter(
                course_id=course_id,
                is_published=True
            )

        return Lesson.objects.filter(
            course_id=course_id,
            is_published=True,
            is_preview=True
        )



class StudentLessonDetailAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer

    def get_object(self):
        course_id = self.kwargs["course_id"]
        lesson_id = self.kwargs["lesson_id"]

        lesson = get_object_or_404(
            Lesson,
            pk=lesson_id,
            course_id=course_id,
            is_published=True
        )

        if lesson.is_preview:
            return lesson

        is_enrolled = Enrollment.objects.filter(
            student=self.request.user,
            course_id=course_id
        ).exists()

        if not is_enrolled:
            raise PermissionDenied("Enroll to access this lesson.")

        return lesson
