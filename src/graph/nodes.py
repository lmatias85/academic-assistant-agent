from src.graph.state import InformationalState
from src.kg import get_knowledge_graph
from src.kg.queries import get_passed_subjects, get_prerequisites
from src.rag import get_rules_vectorstore
from src.rag.retriever import retrieve_rules_context


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
