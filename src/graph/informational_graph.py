from langgraph.graph import StateGraph, END

from src.graph.state import InformationalState
from src.graph.nodes import (
    reasoning_node,
    kg_query_node,
    rag_retrieval_node,
    synthesis_node,
)


def build_informational_graph():
    graph = StateGraph(InformationalState)

    graph.add_node("reasoning", reasoning_node)
    graph.add_node("kg_query", kg_query_node)
    graph.add_node("rag_retrieval", rag_retrieval_node)
    graph.add_node("synthesis", synthesis_node)

    # Centralized, fixed flow
    graph.set_entry_point("reasoning")
    graph.add_edge("reasoning", "kg_query")
    graph.add_edge("kg_query", "rag_retrieval")
    graph.add_edge("rag_retrieval", "synthesis")
    graph.add_edge("synthesis", END)

    return graph.compile()
