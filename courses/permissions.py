from rest_framework.permissions import BasePermission
from users.models import User


class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == User.ROLE_INSTRUCTOR
        )


class IsCourseOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.instructor.user == request.user
