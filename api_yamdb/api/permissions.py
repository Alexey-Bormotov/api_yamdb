from rest_framework import permissions


class OnlyAuthorPermission(permissions.BasePermission):
    message = (
        'Only Author, Moderator, Admin or Superuser is allowed to access.')

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return (request.user.role in ['moderator', 'admin']
                or request.user.bio == 'superuser bio'
                or obj.author == request.user)


class IsAdminPermission(permissions.BasePermission):
    message = 'Only Admin or Superuser is allowed to access.'

    def has_permission(self, request, view):
        return (request.user.role == 'admin'
                or request.user.bio == 'superuser bio')


class AdminOrReadOnlyPermission(permissions.BasePermission):
    message = 'Only Admin or Superuser is allowed to access.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return (request.user.role == 'admin'
                or request.user.bio == 'superuser bio')
