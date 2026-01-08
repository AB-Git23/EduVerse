from django.urls import path
from .views import (
    InstructorLessonListCreateAPIView,
    InstructorLessonDetailAPIView,
    LessonPublishAPIView,
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
]
