"""Here all costume permissions of the project"""
from rest_framework import permissions


class IfAuthenticatedReadAndCreate(permissions.BasePermission):
    """
    Global permission check whether user authenticated
    to give him permission to read posts and create his own.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                    request.method in permissions.SAFE_METHODS
                    or request.method == "POST"
            )
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named 'owner'.
        return obj.owner == request.user
