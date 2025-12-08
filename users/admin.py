from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from .models import User, StudentProfile, InstructorProfile
from .serializers import InstructorProfileSerializer



@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ('email', 'username', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.register(StudentProfile)
admin.site.register(InstructorProfile)


class InstructorReviewViewSet(viewsets.ModelViewSet):
    """
    Admin endpoint to list pending instructor profiles and to approve/reject them.
    - list: pending (is_verified=False)
    - retrieve: get one profile
    - approve: POST /.../{pk}/approve/
    - reject: POST /.../{pk}/reject/ with optional reason
    """
    permission_classes = [IsAdminUser]
    serializer_class = InstructorProfileSerializer

    def get_queryset(self):
        # Only pending by default
        return InstructorProfile.objects.filter(is_verified=False).select_related('user')

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        profile = self.get_object()
        if profile.is_verified:
            return Response({'detail': 'Already verified.'}, status=status.HTTP_400_BAD_REQUEST)

        profile.is_verified = True
        profile.verification_rejected_reason = ''
        profile.verification_reviewed_at = timezone.now()
        profile.save(update_fields=['is_verified', 'verification_rejected_reason', 'verification_reviewed_at'])

        # Explicitly notify the instructor by email (dev: console backend will show)
        try:
            send_mail(
                'Instructor account approved',
                f'Hi {profile.user.username or profile.user.email},\n\nYour instructor account has been approved.',
                settings.DEFAULT_FROM_EMAIL,
                [profile.user.email],
                fail_silently=False,
            )
        except Exception:
            # swallow for dev but log if you have logging
            pass

        return Response({'detail': 'Instructor approved.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        profile = self.get_object()
        reason = request.data.get('reason', '')  # only accept reason

        profile.is_verified = False
        profile.verification_rejected_reason = reason
        profile.verification_reviewed_at = timezone.now()
        profile.save(update_fields=['is_verified', 'verification_rejected_reason', 'verification_reviewed_at'])

        # Notify the instructor about rejection with reason
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
