from django.urls import path, include
from rest_framework_nested import routers
from . import views
from . import admin

router = routers.DefaultRouter()
router.register('register/student', views.StudentRegisterView, basename='student-register')
router.register('register/instructor', views.InstructorRegisterView, basename='instructor-register')
router.register("admin/verification-submissions", views.AdminVerificationSubmissionViewSet, basename="admin-verification-submissions")

urlpatterns = [
    path('', include(router.urls)),
    # path("admin/verification-submissions/<int:submission_id>/approve/", views.ApproveVerificationSubmissionAPIView.as_view()),
    # path("admin/verification-submissions/<int:submission_id>/reject/", views.RejectVerificationSubmissionAPIView.as_view()),
    path("instructor/verification/submit/", views.CreateVerificationSubmissionAPIView.as_view()),
    path("instructor/verification/status/", views.InstructorVerificationStatusAPIView.as_view(),),


]
