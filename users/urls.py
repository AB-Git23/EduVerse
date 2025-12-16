from django.urls import path, include
from rest_framework_nested import routers
from . import views
from . import admin

router = routers.DefaultRouter()
router.register('register/student', views.StudentRegisterView, basename='student-register')
router.register('register/instructor', views.InstructorRegisterView, basename='instructor-register')
router.register('admin/instructor-reviews', views.InstructorReviewViewSet, basename='instructor-reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('profile/upload-verification/', views.UploadVerificationDocumentAPIView.as_view(), name='upload-verification'),

]
