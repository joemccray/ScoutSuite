from rest_framework import permissions
from scout_web.organizations.permissions import IsOrgMember

class OrganizationScopedViewSetMixin:
    """
    A mixin for viewsets that scopes querysets and object creation
    to the user's organization.
    """
    permission_classes = [permissions.IsAuthenticated, IsOrgMember]

    def get_queryset(self):
        user = self.request.user
        organization = user.orgrole_set.first().organization
        return self.queryset.filter(organization=organization)

    def perform_create(self, serializer):
        user = self.request.user
        organization = user.orgrole_set.first().organization
        serializer.save(organization=organization)
