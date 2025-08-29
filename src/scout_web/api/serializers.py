from rest_framework import serializers
from .models import CloudProvider, Account, Scan, Finding, RuleSet, Rule, RuleException
from scout_web.organizations.models import Organization, OrgRole
from .validators import CredentialsSerializer

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class OrgRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgRole
        fields = '__all__'

class CloudProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudProvider
        fields = '__all__'
        read_only_fields = ('organization',)

class AccountSerializer(serializers.ModelSerializer):
    credentials = CredentialsSerializer(write_only=True)

    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ('organization',)


class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = '__all__'
        read_only_fields = ('organization',)

class FindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finding
        fields = '__all__'
        read_only_fields = ('organization',)

class RuleSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleSet
        fields = '__all__'
        read_only_fields = ('organization',)

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'
        read_only_fields = ('organization',)

class RuleExceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleException
        fields = '__all__'
        read_only_fields = ('organization',)
