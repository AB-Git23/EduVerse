from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import InstructorProfile, StudentProfile, User

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password', 'role')


class CustomUserSerializer(UserSerializer):
    profile = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'role', 'profile')

    def get_profile(self, obj):
        if obj.role == User.ROLE_STUDENT:
            try:
                profile = obj.student_profile
                return {
                    'batch': profile.batch,
                    'enrollment_date': profile.enrollment_date,
                }
            except:
                return None
        elif obj.role == User.ROLE_INSTRUCTOR:
            try:
                profile = obj.instructor_profile
                return {
                    'bio': profile.bio,
                    'expertise': profile.expertise,
                }
            except:
                return None
        return None


class StudentProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = StudentProfile
        fields = ('user', 'enrollment_date', 'batch')


class InstructorProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = InstructorProfile
        fields = ('user', 'bio', 'expertise')


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


class IntructorRegisterSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(required=False, write_only=True)
    expertise = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'bio', 'expertise')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        bio = validated_data.pop('bio', '')
        expertise = validated_data.pop('expertise', '')

        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username') or validated_data['email'],
            password=validated_data['password'],
            role=User.ROLE_INSTRUCTOR,
        )

        InstructorProfile.objects.create(
            user=user,
            bio=bio,
            expertise=expertise
        )

        return user
