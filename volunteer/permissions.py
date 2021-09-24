from rest_framework import permissions

from authentication.enums import UserType


class IsVolunteer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == UserType.VIO

    def has_object_permission(self, request, view, obj):
        return request.user.user_type == UserType.VIO
