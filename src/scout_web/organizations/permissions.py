from rest_framework import permissions

class IsOrgMember(permissions.BasePermission):
    """
    Allows access only to users who are members of an organization.
    """

    def has_permission(self, request, view):
        return hasattr(request.user, 'orgrole_set') and request.user.orgrole_set.exists()
