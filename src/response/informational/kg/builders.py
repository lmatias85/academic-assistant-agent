import networkx as nx

from src.response.informational.kg.db_reader import fetch_prerequisites


def build_prerequisite_graph() -> nx.DiGraph:
    """
    Builds a directed graph of subject prerequisites.
    Edge: required_subject -> subject
    """
    g = nx.DiGraph()

    for subject, required in fetch_prerequisites():
        g.add_edge(required, subject)

    return g
