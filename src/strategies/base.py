from abc import ABC, abstractmethod
from src.agent.types import AgentDecision


class RouteStrategy(ABC):
    """
    Base interface for route execution strategies.
    """

    @abstractmethod
    def execute(self, user_input: str, decision: AgentDecision) -> None:
        pass
