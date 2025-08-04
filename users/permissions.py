from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Разрешает доступ только владельцу привычки"""

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "owner"):
            return obj.owner == request.user
        return False
