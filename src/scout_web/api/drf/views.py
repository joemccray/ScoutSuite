from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from pathlib import Path
from django.conf import settings

from scout_web.api.agents.registry import AGENTS, QA_AGENTS
from scout_web.api.agents.base import run_agent_single
from scout_web.api.workflows.runner import execute_workflow
from .serializers import RunAgentSerializer, RunWorkflowSerializer

class AgentsViewSet(viewsets.ViewSet):
    def list(self, request):
        data = [{"id": k, "has_qa": k in QA_AGENTS} for k in AGENTS.keys()]
        return Response(data)

    @action(detail=False, methods=["post"])
    def run(self, request):
        ser = RunAgentSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        agent_id = ser.validated_data["agent_id"]
        payload = ser.validated_data.get("payload", {})
        run_with_qa = ser.validated_data["run_with_qa"]
        agent = AGENTS[agent_id]
        out = run_agent_single(agent, description=str(payload.get("task", "General task")))
        result = {"agent_output": out}
        if run_with_qa and agent_id in QA_AGENTS:
            qa = QA_AGENTS[agent_id]
            qa_out = run_agent_single(qa, description=f"Validate output:\n{out}")
            result["qa_output"] = qa_out
        return Response(result, status=status.HTTP_200_OK)

class WorkflowsViewSet(viewsets.ViewSet):
    def list(self, request):
        specs_dir = Path(settings.BASE_DIR) / "api" / "workflows" / "specs"
        items = [{"id": p.stem, "path": str(p)} for p in specs_dir.glob("*.yaml")]
        return Response(items)

    @action(detail=False, methods=["post"])
    def run(self, request):
        ser = RunWorkflowSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        trace = execute_workflow(ser.validated_data["spec_path"])
        return Response(trace, status=status.HTTP_200_OK)
