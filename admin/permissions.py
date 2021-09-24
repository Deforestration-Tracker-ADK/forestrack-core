from rest_framework import permissions

from authentication.enums import UserType


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == UserType.ADMIN

    def has_object_permission(self, request, view, obj):
        return request.user.user_type == UserType.ADMIN
