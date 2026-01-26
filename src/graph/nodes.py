from src.graph.state import InformationalState
from src.kg import get_knowledge_graph
from src.kg.queries import get_passed_subjects, get_prerequisites


def reasoning_node(state: InformationalState) -> InformationalState:
    """
    Initial reasoning node.
    For now, it simply passes the user input forward.
    """
    return state


def kg_query_node(state: InformationalState) -> InformationalState:
    """
    Query the Knowledge Graph for structured academic data.
    """
    graph = get_knowledge_graph()

    student_id = "student:john_doe"
    target_subject = "subject:physics_2"

    passed = get_passed_subjects(graph, student_id)
    prerequisites = get_prerequisites(graph, target_subject)

    state["kg_context"] = (
        f"Passed subjects: {passed}. " f"Prerequisites for Physics II: {prerequisites}."
    )

    return state


def rag_retrieval_node(state: InformationalState) -> InformationalState:
    """
    Retrieve relevant academic rules using RAG.
    Stub implementation.
    """
    state["rag_context"] = "RAG context: academic rules (stub)"
    return state


def synthesis_node(state: InformationalState) -> InformationalState:
    """
    Combine KG and RAG contexts into a final answer.
    Stub implementation.
    """
    state["answer"] = (
        f"Answer based on:\n" f"- {state['kg_context']}\n" f"- {state['rag_context']}"
    )
    return state
