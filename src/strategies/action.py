from src.agent.types import AgentDecision
from src.strategies.base import RouteStrategy


class ActionStrategy(RouteStrategy):
    """
    Strategy responsible for handling action requests
    via the MCP Server.
    """

    def execute(self, user_input: str, decision: AgentDecision) -> None:
        print("\n[Action]")
        print("Action handling via MCP Server (not implemented yet).")
