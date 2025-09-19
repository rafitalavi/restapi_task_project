from rest_framework import permissions


class IsAllowedToEditTaskListElseNone(permissions.BasePermission):
    """
    Only the creator can edit a task list. Everyone can read.
    """

    def has_permission(self, request, view):
        # Read is allowed for anyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write requires authentication
        if not request.user.is_anonymous:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Allow read for anyone
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        # Allow edit only for creator
        return request.user.profile == obj.created_by


class IsAllowedToEditTaskElseNone(permissions.BasePermission):
    """
    Only team members can edit a task. Everyone can read.
    """

    def has_permission(self, request, view):
       
        # Write requires authentication
        if not request.user.is_anonymous:
            return request.user.profile.team is not None
        return False
       

    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        return  request.user.profile.team == obj.task_list.team


class IsAllowedToEditAttachmentElseNone(permissions.BasePermission):
    """
    Only team members can edit an attachment. Everyone can read.
    """

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.profile.team is not None
        return  request.user.profile.team == obj.task.task_list.team
