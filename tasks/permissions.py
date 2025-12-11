# tasks/permissions.py
from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to allow:
    - Admin to access any task
    - Users to access only their own tasks
    """
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="Admin").exists() or request.user.is_superuser:
            return True
        return obj.owner == request.user
