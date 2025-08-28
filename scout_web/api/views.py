from rest_framework import viewsets
from .models import CloudProvider, Account, Scan, Finding
from .serializers import CloudProviderSerializer, AccountSerializer, ScanSerializer, FindingSerializer

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
