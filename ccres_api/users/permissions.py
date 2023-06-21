from rest_framework.permissions import BasePermission


class IsEditor(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Editor".lower()).exists()
