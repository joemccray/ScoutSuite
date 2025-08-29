from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CloudProvider, Account, Scan, Finding, RuleSet, Rule, RuleException
from .serializers import (
    CloudProviderSerializer, AccountSerializer, ScanSerializer, FindingSerializer,
    RuleSetSerializer, RuleSerializer, RuleExceptionSerializer
)
from .validators import ScanConfigurationSerializer
from .tasks import run_scan

class CloudProviderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows cloud providers to be viewed.
    """
    queryset = CloudProvider.objects.all()
    serializer_class = CloudProviderSerializer

class AccountViewSet(viewsets.ModelViewSet):
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
        print("Scan action called")
        account = self.get_object()

        # Validate the scan configuration
        config_serializer = ScanConfigurationSerializer(data=request.data.get('configuration', {}))
        config_serializer.is_valid(raise_exception=True)
        config = config_serializer.validated_data

        # Create a new Scan object
        new_scan = Scan.objects.create(account=account, status='PENDING', configuration=config)

        # Trigger the Celery task after the transaction is committed
        transaction.on_commit(lambda: run_scan.delay(new_scan.id))

        return Response({'status': 'scan_started', 'scan_id': new_scan.id})

class ScanViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows scans to be viewed.
    """
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer

class FindingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows findings to be viewed.
    """
    queryset = Finding.objects.all()
    serializer_class = FindingSerializer

class RuleSetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rulesets to be viewed or edited.
    """
    queryset = RuleSet.objects.all()
    serializer_class = RuleSetSerializer

class RuleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rules to be viewed or edited.
    """
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer

class RuleExceptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows exceptions to be viewed or edited.
    """
    queryset = RuleException.objects.all()
    serializer_class = RuleExceptionSerializer
