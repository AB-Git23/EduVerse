from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import permissions, generics, status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import QueryDict
from .permissions import IsInstructor, IsStudent
from .serializers import InstructorProfileSerializer, StudentProfileSerializer, StudentRegisterSerializer, InstructorRegisterSerializer, RejectReasonSerializer, EmptySerializer, InstructorVerificationDocumentSerializer
from .models import StudentProfile, InstructorProfile, InstructorVerificationDocument
from .validators import validate_document_file

User = get_user_model()


class StudentRegisterView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = StudentRegisterSerializer
    permission_classes = [permissions.AllowAny]


class InstructorRegisterView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = InstructorRegisterSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

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
        serializer = serializer_class(
            instance, data=data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class InstructorReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = InstructorProfileSerializer

    def get_queryset(self):
        return InstructorProfile.objects.filter(is_verified=False).select_related('user')

    def get_serializer_class(self):
        if self.action == 'reject':
            return RejectReasonSerializer
        if self.action == 'approve':
            return EmptySerializer
        return InstructorProfileSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        profile = self.get_object()
        profile.is_verified = True
        profile.verification_rejected_reason = ''
        profile.verification_reviewed_at = timezone.now()
        profile.save(update_fields=[
                     'is_verified', 'verification_rejected_reason', 'verification_reviewed_at'])

        try:
            send_mail(
                'Instructor account approved',
                f'Hi {profile.user.username or profile.user.email},\n\nYour instructor account has been approved.',
                settings.DEFAULT_FROM_EMAIL,
                [profile.user.email],
                fail_silently=False,
            )
        except Exception:
            pass

        return Response({'detail': 'Instructor approved.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reason = serializer.validated_data['reason']

        profile = self.get_object()
        profile.is_verified = False
        profile.verification_rejected_reason = reason
        profile.verification_reviewed_at = timezone.now()
        profile.save(update_fields=[
                     'is_verified', 'verification_rejected_reason', 'verification_reviewed_at'])

        try:
            send_mail(
                'Instructor verification rejected',
                f'Hi {profile.user.username or profile.user.email},\n\n'
                f'Your instructor verification request was rejected.\n\nReason: {reason}',
                settings.DEFAULT_FROM_EMAIL,
                [profile.user.email],
                fail_silently=False,
            )
        except Exception:
            pass

        return Response({'detail': 'Instructor rejected.', 'reason': reason}, status=status.HTTP_200_OK)



class UploadVerificationDocumentAPIView(APIView):
    """
    Accepts one or more files via 'verification_documents' form field.
    - Only instructors allowed.
    - Validates each file.
    - Creates InstructorVerificationDocument rows.
    - Updates InstructorProfile: sets is_verified=False, clears rejection reason,
      updates verification_requested_at.
    - Returns the InstructorProfileSerializer (with documents list).
    """
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.role != User.ROLE_INSTRUCTOR:
            return Response({'detail': 'Only instructors can upload verification documents.'}, status=status.HTTP_403_FORBIDDEN)

        # support either multiple files via 'verification_documents' or 'verification_document'
        files = request.FILES.getlist('verification_documents')
        if not files:
            files = request.FILES.getlist('verification_document')

        if not files:
            return Response({'detail': 'No files provided. Use "verification_documents" (multi) or "verification_document" (single).'}, status=status.HTTP_400_BAD_REQUEST)

        profile, _ = InstructorProfile.objects.get_or_create(user=user)

        created_docs = []
        for f in files:
            try:
                validate_document_file(f)
            except Exception as e:
                # return validation error for the offending file (abort entire upload)
                return Response({'detail': f'File validation error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

            doc = InstructorVerificationDocument(profile=profile, document=f)
            doc.save()
            created_docs.append(doc)

        # update profile to pending
        profile.is_verified = False
        profile.verification_rejected_reason = ''
        profile.verification_requested_at = timezone.now()
        # Optionally update the legacy single-file field to the most recent
        # profile.verification_document = created_docs[-1].document
        profile.save(update_fields=['is_verified', 'verification_rejected_reason', 'verification_requested_at'])

        # Return updated profile data
        serializer = InstructorProfileSerializer(profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)