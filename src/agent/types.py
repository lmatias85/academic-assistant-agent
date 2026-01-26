from enum import Enum
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional, Dict, Any


class Route(str, Enum):
    INFORMATIONAL = "informational"
    ACTION = "action"


@dataclass(frozen=True)
class AgentDecision:
    route: Route
    reason: str
    arguments: Optional[Dict[str, Any]] = None


class LLMActionArguments(BaseModel):
    student_name: str
    subject_name: str


class LLMDecision(BaseModel):
    route: Route
    reason: str
    arguments: Optional[LLMActionArguments] = None
