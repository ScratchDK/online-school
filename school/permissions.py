from rest_framework import permissions
from rest_framework.permissions import IsAdminUser


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="moders").exists()
        )


class IsAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return IsAdminUser().has_permission(
            request, view
        ) or IsModerator().has_permission(request, view)


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
