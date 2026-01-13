from django.urls import path
from .views import StudentEnrollmentListCreateAPIView

urlpatterns = [
    path(
        "student/enrollments/",
        StudentEnrollmentListCreateAPIView.as_view(),
        name="student-enrollments",
    ),
    
]

