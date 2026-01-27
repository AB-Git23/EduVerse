from django.urls import path
from .views import (
    InstructorLessonListCreateAPIView,
    InstructorLessonDetailAPIView,
    LessonPublishAPIView,
    StudentLessonDetailAPIView,
    StudentLessonListAPIView,
)

urlpatterns = [
    path(
        "instructor/courses/<int:course_id>/lessons/",
        InstructorLessonListCreateAPIView.as_view(),
        name="instructor-lessons",
    ),
    path(
        "instructor/courses/<int:course_id>/lessons/<int:lesson_id>/",
        InstructorLessonDetailAPIView.as_view(),
        name="lesson-detail",
    ),
    path(
        "instructor/courses/<int:course_id>/lessons/<int:lesson_id>/publish/",
        LessonPublishAPIView.as_view(),
        name="lesson-publish",
    ),
    path(
        "student/courses/<int:course_id>/lessons/",
        StudentLessonListAPIView.as_view(),
        name="student-lessons",
    ),
    path(
        "student/courses/<int:course_id>/lessons/<int:lesson_id>/",
        StudentLessonDetailAPIView.as_view(),
        name="student-lesson-detail",
    ),
]
