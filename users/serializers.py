from django.conf import settings
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from django.utils import timezone

from .validators import validate_document_file
from .models import InstructorProfile, StudentProfile, User

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password', 'role')


class CustomUserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'role')
        extra_kwargs = {
            'role': {'read_only': True},
        }


class StudentProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = ('user', 'enrollment_date', 'batch')


class InstructorProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    verification_document_url = serializers.SerializerMethodField()

    class Meta:
        model = InstructorProfile
        fields = ('id', 'user', 'bio', 'expertise', 'is_verified', 'verification_document_url', 'verification_requested_at', 'verification_rejected_reason', 'verification_reviewed_at')

        read_only_fields = (
            'is_verified',
            'verification_requested_at',
            'verification_rejected_reason',
            'verification_reviewed_at',
            'verification_document_url',
            'verification_reviewed_at',
            'user',
        )

    def get_verification_document_url(self, obj):
        request = self.context.get('request')
        if obj.verification_document:
            if request:
                return request.build_absolute_uri(obj.verification_document.url)
            return obj.verification_document.url
        return None


class StudentRegisterSerializer(serializers.ModelSerializer):
    batch = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'batch')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        batch = validated_data.pop('batch', '')

        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username') or validated_data['email'],
            password=validated_data['password'],
            role=User.ROLE_STUDENT,
        )

        StudentProfile.objects.create(user=user, batch=batch)
        return user
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value



class InstructorRegisterSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(required=False, write_only=True)
    expertise = serializers.CharField(required=False, write_only=True)
    verification_document = serializers.FileField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'bio', 'expertise', 'verification_document')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        bio = validated_data.pop('bio', '')
        expertise = validated_data.pop('expertise', '')
        document = validated_data.pop('verification_document', None)

        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username') or validated_data['email'],
            password=validated_data['password'],
            role=User.ROLE_INSTRUCTOR,
        )

        profile = InstructorProfile.objects.create(
            user=user,
            bio=bio,
            expertise=expertise,
        )
        if document:
            validate_document_file(document)
            profile.verification_document = document
            profile.verification_requested_at = timezone.now()
            profile.save(update_fields=['verification_document', 'verification_requested_at'])

        return user

    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    

class RejectReasonSerializer(serializers.Serializer):
    reason = serializers.CharField(required=True, allow_blank=False)
