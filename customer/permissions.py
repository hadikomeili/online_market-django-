from rest_framework import permissions


class IsSuperuserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj.owner, request.user)
        return request.user == obj.owner
