from django.urls import path
from .views import (
    CoursePublishAPIView,
    InstructorCourseDetailAPIView,
    InstructorCourseListCreateAPIView,
    PublicCourseDetailAPIView,
    PublicCourseListAPIView,
    InstructorSectionListCreateAPIView,
    CourseCompletionAPIView,
)

urlpatterns = [
    path(
        "instructor/courses/",
        InstructorCourseListCreateAPIView.as_view(),
        name="instructor-courses",
    ),
    path(
        "instructor/courses/<int:pk>/",
        InstructorCourseDetailAPIView.as_view(),
        name="instructor-course-detail",
    ),
    path(
        "instructor/courses/<int:pk>/publish/",
        CoursePublishAPIView.as_view(),
        name="course-publish",
    ),
    path(
        "instructor/courses/<int:course_id>/sections/",
        InstructorSectionListCreateAPIView.as_view(),
        name="instructor-sections",
    ),
    path(
        "public/courses/",
        PublicCourseListAPIView.as_view(),
        name="public-courses",
    ),
    path(
        "public/courses/<int:pk>/",
        PublicCourseDetailAPIView.as_view(),
        name="public-course-detail",
    ),
    path(
        "student/courses/<int:course_id>/completion/",
        CourseCompletionAPIView.as_view(),
        name="course-completion",
    ),
]
