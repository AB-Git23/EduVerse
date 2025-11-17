from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('register/student', views.StudentRegisterView, basename='student-register')
router.register('register/instructor', views.InstructorRegisterView, basename='instructor-register')
router.register('profile/student', views.StudentProfileDetail, basename='student-profile')
router.register('profile/instructor', views.InstructorProfileDetail, basename='instructor-profile')


urlpatterns = router.urls
