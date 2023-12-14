from rest_framework import permissions


class AuthorOnly(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj == request.user
