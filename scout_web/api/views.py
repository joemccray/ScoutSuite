from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CloudProvider, Account, Scan, Finding
from .serializers import CloudProviderSerializer, AccountSerializer, ScanSerializer, FindingSerializer
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

    @action(detail=True, methods=['post'])
    def scan(self, request, pk=None):
        """
        Triggers a new scan for the account.
        """
        account = self.get_object()

        # Create a new Scan object
        new_scan = Scan.objects.create(account=account, status='PENDING')

        # Trigger the Celery task
        run_scan.delay(new_scan.id)

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
