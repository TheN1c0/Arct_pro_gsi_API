
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Permiso que permite a los administradores acceder a las vistas.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class IsCollaborator(permissions.BasePermission):
    """
    Permiso que permite a los colaboradores acceder a las vistas.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_admin
