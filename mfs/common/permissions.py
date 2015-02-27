from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from mfs.common.constants import ADMIN_GROUP


def has_group(user, group):
    return user.groups.filter(name=group).count()


def check_admin(user):
    if not (user.is_staff or has_group(user, ADMIN_GROUP)):
        raise PermissionDenied


class IsAdminGroup(BasePermission):
    def has_permission(self, request, view):
        check_admin(request.user)
        return True


class IsAuthenticatedOrOwner(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return True


class IsAuthenticatedCreateAllowed(BasePermission):
    def has_permission(self, request, view):
        is_user_creation = (len(request.path.strip('/').split('/')) <= 1)
        if request.method in ['POST'] and is_user_creation:
            return True
        if not request.user.is_authenticated():
            return False
        return True