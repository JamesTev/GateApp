from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    """Custom permission class to only allow superuser to add/update/delete User records"""

    def has_permission(self, request, view):
        """Return True if permission is granted to superuser"""
        if request.user.is_superuser:
            return True
        return False



