import networkx as nx


def get_passed_subjects(graph: nx.DiGraph, student_id: str) -> list[str]:
    """
    Return a list of subjects passed by the given student.
    """
    passed = []

    for _, target, data in graph.out_edges(student_id, data=True):
        if data.get("relation") == "PASSED":
            passed.append(target)

    return passed


def get_prerequisites(graph: nx.DiGraph, subject_id: str) -> list[str]:
    """
    Return prerequisite subjects for a given subject.
    """
    prerequisites = []

    for source, _, data in graph.in_edges(subject_id, data=True):
        if data.get("relation") == "PREREQUISITE":
            prerequisites.append(source)

    return prerequisites
