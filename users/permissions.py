from rest_framework import permissions


class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'instructor'


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'student'
