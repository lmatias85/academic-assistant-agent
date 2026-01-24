from enum import Enum
from dataclasses import dataclass
from pydantic import BaseModel


class Route(str, Enum):
    INFORMATIONAL = "informational"
    ACTION = "action"


@dataclass(frozen=True)
class AgentDecision:
    route: Route
    reason: str


class LLMDecision(BaseModel):
    route: Route
    reason: str