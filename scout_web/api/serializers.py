from rest_framework import serializers
from .models import CloudProvider, Account, Scan, Finding, RuleSet, Rule, RuleException
from .validators import CredentialsSerializer

class CloudProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudProvider
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    credentials = CredentialsSerializer(write_only=True)

    class Meta:
        model = Account
        fields = '__all__'


class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = '__all__'

class FindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finding
        fields = '__all__'

class RuleSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleSet
        fields = '__all__'

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'

class RuleExceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleException
        fields = '__all__'
