from rest_framework import permissions


class IsSuperuserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsOwnerAddressPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.username == obj.owner.username


class IsOwnerCartPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.username == obj.cart.customer.username