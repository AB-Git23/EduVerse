from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions, generics, status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .permissions import IsInstructor, IsStudent
from .serializers import InstructorProfileSerializer, StudentProfileSerializer, StudentRegisterSerializer, InstructorRegisterSerializer
from .models import StudentProfile, InstructorProfile

User = get_user_model()


class StudentRegisterView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = StudentRegisterSerializer
    permission_classes = [permissions.AllowAny]

class InstructorRegisterView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = InstructorRegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.role == User.ROLE_STUDENT:
            return StudentProfileSerializer
        return InstructorProfileSerializer

    def get_object(self):
        user = self.request.user
        if user.role == User.ROLE_STUDENT:
            profile, _ = StudentProfile.objects.get_or_create(user=user)
            return profile
        profile, _ = InstructorProfile.objects.get_or_create(user=user)
        return profile

    def destroy(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)