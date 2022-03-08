from rest_framework import permissions


class OnlyAuthorPermission(permissions.BasePermission):
    message = 'Only Author is allowed to access.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return permissions.IsAuthenticatedOrReadOnly
        return obj.author == request.user


class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.role == 'admin' or
                request.user.bio == 'superuser bio')


class AdminOrReadOnlyPermission(permissions.BasePermission):
    message = 'Only Admin is allowed to access.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return (request.user.role == 'admin' or
                request.user.bio == 'superuser bio')
