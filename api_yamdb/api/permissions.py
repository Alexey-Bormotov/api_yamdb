from rest_framework import permissions


class OnlyAuthorPermission(permissions.BasePermission):
    message = 'Only Author is allowed to access.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return permissions.IsAuthenticatedOrReadOnly
        return obj.author == request.user