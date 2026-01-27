from src.response.informational.kg.builders import build_prerequisite_graph
from src.response.informational.kg.db_reader import fetch_passed_subjects


def can_enroll(student_name: str, target_subject: str) -> dict:
    """
    Evaluates if a student can enroll based on passed prerequisites.
    """
    passed = set(fetch_passed_subjects(student_name))
    graph = build_prerequisite_graph()

    required = set(graph.predecessors(target_subject))

    missing = required - passed

    return {
        "passed_subjects": sorted(passed),
        "required_subjects": sorted(required),
        "missing_prerequisites": sorted(missing),
        "eligible": len(missing) == 0,
    }
