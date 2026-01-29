from src.response.informational.pipeline.state import InformationalState


def normalize_academic_entities(state: InformationalState) -> None:
    """
    Normalizes academic entities so that subject_name is always populated
    when a course_name refers to a subject-level concept.
    """

    if state.get("subject_name") is None and state.get("course_name"):
        state["subject_name"] = state["course_name"]
