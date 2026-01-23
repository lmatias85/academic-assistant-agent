from src.agent.types import AgentDecision, Route


class PrimaryAgent:
    """
    Primary decision agent.

    Responsible only for deciding whether a user request
    is informational or action-oriented.
    """

    def decide(self, user_input: str) -> AgentDecision:
        """
        Decide which route should handle the user input.

        NOTE:
        This is a stub implementation.
        It will later be replaced by LLM-based reasoning.
        """
        # Temporary deterministic behavior (stub)
        decision = AgentDecision(
            route=Route.INFORMATIONAL,
            reason="Stub decision: defaulting to informational route",
        )

        return decision
