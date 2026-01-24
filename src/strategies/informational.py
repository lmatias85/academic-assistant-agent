from src.agent.types import AgentDecision
from src.graph.informational_graph import build_informational_graph
from src.strategies.base import RouteStrategy


class InformationalStrategy(RouteStrategy):
    """
    Strategy responsible for handling informational queries
    via the centralized RAG + KG graph.
    """

    def __init__(self) -> None:
        self.graph = build_informational_graph()

    def execute(self, user_input: str, decision: AgentDecision) -> None:
        result = self.graph.invoke(
            {
                "user_input": user_input,
                "kg_context": None,
                "rag_context": None,
                "answer": None,
            }
        )

        print("\n[Answer]")
        print(result["answer"])
