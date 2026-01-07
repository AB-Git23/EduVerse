from django.urls import path
from .views import CoursePublishAPIView, InstructorCourseDetailAPIView, InstructorCourseListCreateAPIView

urlpatterns = [
    path("instructor/courses/", InstructorCourseListCreateAPIView.as_view(),name="instructor-courses",),
    path("instructor/courses/<int:pk>/", InstructorCourseDetailAPIView.as_view(), name="instructor-course-detail",),
    path("instructor/courses/<int:pk>/publish/", CoursePublishAPIView.as_view(), name="course-publish",)
]
