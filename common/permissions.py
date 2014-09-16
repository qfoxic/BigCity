from rest_framework.permissions import BasePermission

class IsAdminGroup(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return True

class IsAuthenticatedOrOwner(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return True