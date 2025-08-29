from rest_framework import serializers

class CredentialsSerializer(serializers.Serializer):
    # This is a very basic validator. A real implementation would have
    # provider-specific validation.
    def to_internal_value(self, data):
        if not isinstance(data, dict):
            raise serializers.ValidationError("Credentials must be a dictionary.")
        return data

class ScanConfigurationSerializer(serializers.Serializer):
    services = serializers.ListField(child=serializers.CharField(), required=False)
    skipped_services = serializers.ListField(child=serializers.CharField(), required=False)
    regions = serializers.ListField(child=serializers.CharField(), required=False)
    excluded_regions = serializers.ListField(child=serializers.CharField(), required=False)
    ruleset = serializers.CharField(required=False)

    def to_internal_value(self, data):
        # Allow any other keys to be present, but don't validate them.
        # A more advanced implementation could validate all keys.
        return super().to_internal_value(data)
