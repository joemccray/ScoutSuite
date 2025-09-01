from typing import Any, Dict
from django.conf import settings

from crewai import Agent as CrewAgent, Task as CrewTask, Crew, Process
from crewai_tools import tool

@tool("echo")
def echo_tool(q: str) -> str:
    """Echo back a string (for smoke tests)."""
    return q

def make_agent(name: str, role: str, goal: str, backstory: str, tools=None, verbose=None) -> CrewAgent:
    return CrewAgent(
        role=role,
        goal=goal,
        backstory=backstory,
        tools=tools or [echo_tool],
        verbose=bool(settings.CREWAI_VERBOSE if verbose is None else verbose),
        allow_delegation=False,
    )

def run_agent_single(agent: CrewAgent, description: str) -> str:
    task = CrewTask(description=description, agent=agent, expected_output="Complete, actionable result.")
    crew = Crew(agents=[agent], tasks=[task], process=Process.sequential)
    res = crew.kickoff()
    return str(res)
