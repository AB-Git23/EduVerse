from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('register/student', views.StudentRegisterView, basename='student-register')
router.register('register/instructor', views.InstructorRegisterView, basename='instructor-register')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', views.ProfileDetail.as_view(), name='profile-detail'),

]
