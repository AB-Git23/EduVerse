from django.urls import path
from .views import (
    ReviewCreateAPIView,
    CourseReviewListAPIView,
)

urlpatterns = [
    path(
        "student/reviews/",
        ReviewCreateAPIView.as_view(),
        name="review-create",
    ),
    path(
        "public/courses/<int:course_id>/reviews/",
        CourseReviewListAPIView.as_view(),
        name="course-reviews",
    ),
    path(
        "student/courses/<int:course_id>/reviews/",
        ReviewCreateAPIView.as_view(),
        name="review-create",
    ),

]
