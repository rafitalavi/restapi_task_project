from rest_framework import viewsets, permissions
from .models import Team


class IsTeamManagerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow team managers to edit the team.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to authenticated users.
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the team manager.
        return obj.user.profile == request.manager