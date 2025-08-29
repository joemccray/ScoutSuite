from pydantic import BaseModel, Field
from typing import List, Dict, Any

class Step(BaseModel):
    id: str
    agent: str
    qa_agent: str
    input: Dict[str, Any] = Field(default_factory=dict)
    acceptance: List[str] = Field(default_factory=list)
    max_retries: int = 1
    timeout_s: int = 180

class WorkflowSpec(BaseModel):
    id: str
    name: str
    icp: str
    goal: str
    kpis: Dict[str, Any] = Field(default_factory=dict)
    steps: List[Step]
