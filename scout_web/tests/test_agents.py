from scout_web.api.agents.base import run_agent_single, make_agent

def test_echo_agent_runs():
    a = make_agent(
        name="echo",
        role="Echo",
        goal="Echo queries",
        backstory="Test agent"
    )
    out = run_agent_single(a, "Echo this back to me.")
    assert isinstance(out, str) and len(out) > 0
