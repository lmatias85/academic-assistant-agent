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
        # ⚠️ Versión inicial: input fijo para demostrar el flujo
        input_data = EnrollStudentInput(
            student_name="John Doe",
            subject_name="Physics II",
        )

        result = enroll_student_via_mcp(input_data)

        print("\n[Action Result]")
        print(result.message)
