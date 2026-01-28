from src.response.agent.types_agent import RouterDecision
from src.response.informational.pipeline.state import InformationalState
from src.response.informational.pipeline.informational_graph import (
    build_informational_graph,
)
from src.response.strategies.base import RouteStrategy


class InformationalStrategy(RouteStrategy):
    """
    Strategy responsible for handling informational queries
    via the centralized RAG + KG graph.
    """

    def __init__(self) -> None:
        self.graph = build_informational_graph()

    def execute(self, user_input: str, decision: RouterDecision) -> None:
        initial_state: InformationalState = {
            "user_input": user_input,
            "student_name": None,
            "subject_name": None,
            "course_name": None,
            "kg_context": None,
            "rag_context": None,
            "answer": None,
        }
        result = self.graph.invoke(initial_state)

        print("\n[Answer]")
        print(result["answer"])