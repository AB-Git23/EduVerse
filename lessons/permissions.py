from rest_framework.permissions import BasePermission


class IsCourseOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.course.instructor.user == request.user
