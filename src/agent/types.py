from enum import Enum
from dataclasses import dataclass


class Route(str, Enum):
    INFORMATIONAL = "informational"
    ACTION = "action"


@dataclass(frozen=True)
class AgentDecision:
    route: Route
    reason: str
