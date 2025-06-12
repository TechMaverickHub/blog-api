from rest_framework.permissions import BasePermission

from app.global_constants import GlobalValues


class IsSuperAdmin(BasePermission):
    """
    Allows access only to users with the SuperAdmin role.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role_id == GlobalValues.SUPER_ADMIN.value


class IsUser(BasePermission):
    """
    Allows access only to users with the User role.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role_id == GlobalValues.USER.value


class IsAdmin(BasePermission):
    """
    Allows access only to users with the AdMIN role.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role_id == GlobalValues.ADMIN.value


class IsAdminOrUser(BasePermission):
    """
    Allows access only to users with the AdMIN or USER role.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role_id in [GlobalValues.ADMIN.value,
                                                                                           GlobalValues.USER.value]
