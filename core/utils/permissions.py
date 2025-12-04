from rest_framework.permissions import BasePermission


class NotAuthenticate(BasePermission):
    message = "کاربر لاگین شده نمیتواند دسترسی داشته باشد"

    def has_permission(self, request, view):
        return not (request.user and request.user.is_authenticated)
