from rest_framework import permissions
from rest_framework.views import View, Request
from .models import Schedule


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_superuser

        return request.user.is_doctor


class IsDoctorOwner(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, obj: Schedule
    ) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "DELETE":
            return request.user == obj.doctor

        if not obj.is_available:
            return request.user == obj.user or request.user == obj.doctor

        if obj.is_available:
            return (
                request.user.is_doctor is not True
                or request.user == obj.doctor
                or request.user != obj.user
            )
