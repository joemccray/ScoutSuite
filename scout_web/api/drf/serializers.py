from rest_framework import serializers

class RunAgentSerializer(serializers.Serializer):
    agent_id = serializers.CharField()
    payload = serializers.DictField(child=serializers.JSONField(), required=False)
    run_with_qa = serializers.BooleanField(default=True)

class RunWorkflowSerializer(serializers.Serializer):
    spec_path = serializers.CharField()
