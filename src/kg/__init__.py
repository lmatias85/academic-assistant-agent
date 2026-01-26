from src.kg.graph import create_knowledge_graph
from src.kg.loader import load_sample_data

_graph = create_knowledge_graph()
load_sample_data(_graph)


def get_knowledge_graph():
    return _graph
