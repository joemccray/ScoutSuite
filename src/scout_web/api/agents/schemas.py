from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List

class AgentInput(BaseModel):
    icp: str = Field(..., description="Target ICP identifier")
    task: str = Field(..., description="Concrete job-to-be-done instruction")
    context: Dict[str, Any] = Field(default_factory=dict)

class AgentOutput(BaseModel):
    success: bool
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class QAInput(BaseModel):
    draft: AgentOutput
    acceptance: List[str] = Field(default_factory=list)

class QAOutput(BaseModel):
    approved: bool
    notes: str
    corrections: Optional[AgentOutput] = None
