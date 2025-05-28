from rest_framework import permissions


class IsOrderOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an order to access it.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
