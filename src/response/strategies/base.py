from abc import ABC, abstractmethod
from response.agent.types_agent import RouterDecision


class RouteStrategy(ABC):
    """
    Base interface for route execution strategies.
    """

    @abstractmethod
    def execute(self, user_input: str, decision: RouterDecision) -> None:
        pass
