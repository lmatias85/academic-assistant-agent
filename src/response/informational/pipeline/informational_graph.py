from langgraph.graph import StateGraph, END

from src.response.informational.pipeline.state import InformationalState
from src.response.informational.pipeline.nodes import (
    extract_entities_node,
    kg_query_node,
    rag_retrieval_node,
    synthesis_node,
)


def build_informational_graph():
    graph = StateGraph(InformationalState)

    # --- Nodes ---
    graph.add_node("entity_extraction", extract_entities_node)
    graph.add_node("kg_query", kg_query_node)
    graph.add_node("rag_retrieval", rag_retrieval_node)
    graph.add_node("synthesis", synthesis_node)

    # --- Edges ---
    graph.add_edge("entity_extraction", "kg_query")
    graph.add_edge("kg_query", "rag_retrieval")
    graph.add_edge("rag_retrieval", "synthesis")
    graph.add_edge("synthesis", END)

    # --- Entry Point ---
    graph.set_entry_point("entity_extraction")

    return graph.compile()
