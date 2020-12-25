from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.created_by == request.user


class UserRegistration(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return request.method == 'POST'


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
