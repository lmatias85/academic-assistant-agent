from src.graph.state import InformationalState


def reasoning_node(state: InformationalState) -> InformationalState:
    """
    Initial reasoning node.
    For now, it simply passes the user input forward.
    """
    return state


def kg_query_node(state: InformationalState) -> InformationalState:
    """
    Query the Knowledge Graph.
    Stub implementation.
    """
    state["kg_context"] = "KG context: structured academic data (stub)"
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
