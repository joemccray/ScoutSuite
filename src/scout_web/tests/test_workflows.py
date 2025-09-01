from scout_web.api.workflows.runner import execute_workflow
from pathlib import Path

def test_execute_workflow(tmp_path):
    p = tmp_path / "wf.yaml"
    p.write_text("""
id: "wf-smoke"
name: "Smoke"
icp: "software_pm"
goal: "Test"
steps:
  - id: "s1"
    agent: "cloud_asset_discovery"
    qa_agent: "qa_cloud_asset_discovery"
    input:
      task: "Say hello."
    acceptance: ["Say hello"]
""", encoding="utf-8")
    trace = execute_workflow(str(p))
    assert trace["workflow"] == "wf-smoke"
    assert len(trace["steps"]) == 1
