from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions, generics, status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import QueryDict
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
    
    def perform_update(self, serializer):
        # This method runs the actual save; serializer already respects read_only_fields.
        serializer.save()

    def update(self, request, *args, **kwargs):
        """
        Prevent non-staff users from modifying verification metadata.
        Create a cleaned data dict and pass it to serializer instead of assigning request.data.
        """
        protected_keys = {
            'is_verified',
            'verification_requested_at',
            'verification_rejected_reason',
            'verification_reviewed_at',
            'verification_document',  # handle uploads via a dedicated endpoint
        }

        # Get object and serializer class as usual
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = self.get_serializer_class()

        # Build a cleaned copy of incoming data
        if isinstance(request.data, QueryDict):
            data = request.data.copy()
        else:
            # ensure we work with a plain dict so we can pop safely
            data = dict(request.data)

        if not request.user.is_staff:
            for key in protected_keys:
                data.pop(key, None)

        # Now validate and save using serializer with the cleaned data
        serializer = serializer_class(instance, data=data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)