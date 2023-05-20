from rest_framework import permissions


class IsAuthorOrAdminOrModeratorOrReadOnly(permissions.BasePermission):
    """
    Разрешает только авторам отзывов и комментариев изменять или удалять их.
    Эти методы доступны также администраторам, модераторам и суперюзеру.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
            or request.user.is_superuser
        )


class IsAdmin(permissions.BasePermission):
    """
    Разрешает только администратору и суперюзеру получать и изменять
    данные о пользователях.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_admin
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает только администраторам добавлять и изменять данные
    о произведениях, категориях и жанрах.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False
