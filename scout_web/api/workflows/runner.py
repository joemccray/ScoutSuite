import yaml, time, structlog
from typing import Dict, Any
from .spec_schema import WorkflowSpec
from scout_web.api.agents.registry import AGENTS, QA_AGENTS
from scout_web.api.agents.base import run_agent_single

log = structlog.get_logger()

def load_workflow(path: str) -> WorkflowSpec:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return WorkflowSpec(**data)

def execute_workflow(spec_path: str) -> Dict[str, Any]:
    spec = load_workflow(spec_path)
    trace = {"workflow": spec.id, "steps": []}
    for step in spec.steps:
        agent = AGENTS[step.agent]
        qa = QA_AGENTS[step.qa_agent]
        start = time.time()
        out = run_agent_single(agent, description=str(step.input.get("task", "")))
        qa_out = run_agent_single(qa, description=f"Validate the following output:\n{out}\n\nAcceptance:\n- " + "\n- ".join(step.acceptance))
        elapsed = time.time() - start
        trace["steps"].append({
            "id": step.id,
            "agent": step.agent,
            "qa_agent": step.qa_agent,
            "elapsed_s": elapsed,
            "agent_output": out,
            "qa_output": qa_out,
        })
        log.info("step_completed", step=step.id, elapsed_s=elapsed)
    return trace
