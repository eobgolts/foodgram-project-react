from rest_framework import permissions


class AuthOnly(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated


class AuthorOnly(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        author = getattr(obj, 'author', obj)

        return author == request.user
