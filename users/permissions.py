from rest_framework.views import Request, View
from rest_framework import permissions
from .models import User


class IsAccountOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User):
        if request.method in permissions.SAFE_METHODS and obj.is_doctor:
            return True

        return obj == request.user or request.user.is_superuser


class IsAdminListUsers(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_superuser

        return True
