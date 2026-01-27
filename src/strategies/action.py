from src.agent.types import AgentDecision
from src.strategies.base import RouteStrategy
from src.strategies.tool_registry import TOOL_REGISTRY


class ActionStrategy(RouteStrategy):
    def execute(self, user_input: str, decision: AgentDecision) -> None:
        if decision.tool_name is None:
            print("\n[Action Error] No tool specified.")
            return

        if decision.arguments is None:
            print("\n[Action Error] Missing arguments for action.")
            return

        handler = TOOL_REGISTRY.get(decision.tool_name)
        if handler is None:
            print(f"\n[Action Error] Unknown tool: {decision.tool_name}")
            return

        try:
            message = handler(decision.arguments)
        except Exception as exc:
            print("\n[Action Error]")
            print(str(exc))
            return

        print("\n[Action Result]")
        print(message)
