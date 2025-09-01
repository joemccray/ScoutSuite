from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CloudProvider, Account, Scan, Finding, RuleSet, Rule, RuleException
from scout_web.organizations.models import Organization, OrgRole
from .serializers import (
    CloudProviderSerializer, AccountSerializer, ScanSerializer, FindingSerializer,
    RuleSetSerializer, RuleSerializer, RuleExceptionSerializer,
    OrganizationSerializer, OrgRoleSerializer
)
from .validators import ScanConfigurationSerializer
from .tasks import run_scan
from .mixins import OrganizationScopedViewSetMixin

class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows organizations to be viewed or edited.
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        # Users can only see organizations they are a member of
        return self.queryset.filter(roles__user=self.request.user).distinct()

class OrgRoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows organization roles to be viewed or edited.
    """
    queryset = OrgRole.objects.all()
    serializer_class = OrgRoleSerializer

    def get_queryset(self):
        # Users can only see roles in organizations they are a member of
        user_orgs = Organization.objects.filter(roles__user=self.request.user)
        return self.queryset.filter(organization__in=user_orgs)

class CloudProviderViewSet(OrganizationScopedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows cloud providers to be viewed.
    """
    queryset = CloudProvider.objects.all()
    serializer_class = CloudProviderSerializer

class AccountViewSet(OrganizationScopedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    throttle_scope = 'scan'

    @action(detail=True, methods=['post'])
    def scan(self, request, pk=None):
        """
        Triggers a new scan for the account.
        """
        account = self.get_object()

        # Validate the scan configuration
        config_serializer = ScanConfigurationSerializer(data=request.data.get('configuration', {}))
        config_serializer.is_valid(raise_exception=True)
        config = config_serializer.validated_data

        # Create a new Scan object
        new_scan = Scan.objects.create(
            account=account,
            organization=account.organization,
            status='PENDING',
            configuration=config
        )

        # Trigger the Celery task after the transaction is committed
        transaction.on_commit(lambda: run_scan.delay(new_scan.id))

        return Response({'status': 'scan_started', 'scan_id': new_scan.id})

class ScanViewSet(OrganizationScopedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows scans to be viewed.
    """
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer

class FindingViewSet(OrganizationScopedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows findings to be viewed.
    """
    queryset = Finding.objects.all()
    serializer_class = FindingSerializer

class RuleSetViewSet(OrganizationScopedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows rulesets to be viewed or edited.
    """
    queryset = RuleSet.objects.all()
    serializer_class = RuleSetSerializer

class RuleViewSet(OrganizationScopedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows rules to be viewed or edited.
    """
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer

class RuleExceptionViewSet(OrganizationScopedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows exceptions to be viewed or edited.
    """
    queryset = RuleException.objects.all()
    serializer_class = RuleExceptionSerializer
