from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from django.contrib.auth import get_user_model
from .permissions import IsInstructor, IsStudent
from .serializers import InstructorProfileSerializer, StudentProfileSerializer, StudentRegisterSerializer, IntructorRegisterSerializer
from .models import StudentProfile, InstructorProfile

User = get_user_model()


class StudentRegisterView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = StudentRegisterSerializer
    permission_classes = [permissions.AllowAny]


class InstructorRegisterView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = IntructorRegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.role == User.ROLE_STUDENT:
            return StudentProfileSerializer
        return InstructorProfileSerializer

    def get_object(self):
        if self.request.user.role == User.ROLE_STUDENT:
            return self.request.user.student_profile
        return self.request.user.instructor_profile
    
    def destroy(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
