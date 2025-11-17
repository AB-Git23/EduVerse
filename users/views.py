from rest_framework.viewsets import ModelViewSet, generics
from rest_framework import permissions
from django.contrib.auth import get_user_model
from .serializers import InstructorProfileSerializer, StudentProfileSerializer, StudentRegisterSerializer, IntructorRegisterSerializer


class StudentRegisterView(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = StudentRegisterSerializer
    permission_classes = [permissions.AllowAny]


class InstructorRegisterView(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = IntructorRegisterSerializer
    permission_classes = [permissions.AllowAny]


class StudentProfileDetail(ModelViewSet):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.student_profile


class InstructorProfileDetail(ModelViewSet):
    serializer_class = InstructorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.instructor_profile
