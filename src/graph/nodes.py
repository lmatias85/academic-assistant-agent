from src.graph.state import InformationalState
from src.kg.queries import can_enroll
from src.rag import get_rules_vectorstore
from src.rag.retriever import retrieve_rules_context


def reasoning_node(state: InformationalState) -> InformationalState:
    """
    Initial reasoning node.
    For now, it simply passes the user input forward.
    """
    return state


def kg_query_node(state: InformationalState) -> InformationalState:
    # ⚠️ Versión inicial: valores fijos para demostrar
    student_name = "John Doe"
    target_subject = "Physics II"

    result = can_enroll(student_name, target_subject)

    state["kg_context"] = (
        f"Student: {student_name}\n"
        f"Passed subjects: {result['passed_subjects']}\n"
        f"Required subjects: {result['required_subjects']}\n"
        f"Missing prerequisites: {result['missing_prerequisites']}\n"
        f"Eligible: {result['eligible']}"
    )

    return state


def rag_retrieval_node(state: InformationalState) -> InformationalState:
    """
    Retrieve relevant academic rules using RAG (FAISS).
    """
    vectorstore = get_rules_vectorstore()

    user_query = state["user_input"]
    rules_context = retrieve_rules_context(vectorstore, user_query)

    state["rag_context"] = rules_context
    return state


def synthesis_node(state: InformationalState) -> InformationalState:
    """
    Combine KG and RAG contexts into a final answer.
    Stub implementation.
    """
    state["answer"] = (
        "Based on structured data and academic rules:\n\n"
        f"[Knowledge Graph]\n{state['kg_context']}\n\n"
        f"[Academic Rules]\n{state['rag_context']}"
    )
    return state
