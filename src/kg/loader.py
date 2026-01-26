import networkx as nx


def load_sample_data(graph: nx.DiGraph) -> None:
    """
    Load sample academic data into the Knowledge Graph.
    """

    # Students
    graph.add_node(
        "student:john_doe", type="student", name="John Doe", status="REGULAR"
    )

    # Subjects
    graph.add_node("subject:math_1", type="subject", name="Math I")
    graph.add_node("subject:physics_2", type="subject", name="Physics II")

    # Relationships
    graph.add_edge("student:john_doe", "subject:math_1", relation="PASSED")
    graph.add_edge("subject:math_1", "subject:physics_2", relation="PREREQUISITE")
