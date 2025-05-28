from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
    IsAuthenticated,
)


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class IsAdminUserOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_staff


class IsTicketOwner(BasePermission):
    """
    Custom permission to only allow owners of a ticket to view or modify it.
    A user is considered an owner if the ticket is in one of their orders.
    """

    def has_object_permission(self, request, view, obj):

        if not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return True
        return obj.orders.filter(user=request.user).exists()

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
