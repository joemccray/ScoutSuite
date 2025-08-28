from rest_framework import serializers
from .models import CloudProvider, Account, Scan, Finding

class CloudProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudProvider
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        # In a real app, you wouldn't expose credentials like this.
        # This is just for the initial setup.
        extra_kwargs = {'credentials': {'write_only': True}}


class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = '__all__'

class FindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finding
        fields = '__all__'
