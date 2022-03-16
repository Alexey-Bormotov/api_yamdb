from rest_framework import permissions


class IsAuthorPermission(permissions.BasePermission):
    message = (
        'Only Author, Moderator, Admin or Superuser is allowed to access.')

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role in ['moderator', 'admin']
                or request.user.is_superuser
                or obj.author == request.user)


class IsAdminPermission(permissions.BasePermission):
    message = 'Only Admin or Superuser is allowed to access.'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


class IsReadOnlyPermission(permissions.BasePermission):
    message = 'Only Admin or Superuser is allowed to access.'

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
