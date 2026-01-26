from typing import Any

from pydantic import ValidationError

from src.agent.types import AgentDecision
from src.mcp.client import enroll_student_via_mcp
from src.mcp.schemas import EnrollStudentInput
from src.strategies.base import RouteStrategy


class ActionStrategy(RouteStrategy):
    """
    Strategy responsible for handling action requests
    via the MCP Server.
    """

    def execute(self, user_input: str, decision: AgentDecision) -> None:
        if decision.arguments is None:
            print("\n[Action Error]")
            print(
                "The action request is missing required arguments "
                "and cannot be executed."
            )
            return

        try:
            input_data = EnrollStudentInput(**decision.arguments)
        except ValidationError as exc:
            print("\n[Action Error]")
            print("Invalid action arguments:")
            print(exc)
            return

        result = enroll_student_via_mcp(input_data)

        print("\n[Action Result]")
        print(result.message)
