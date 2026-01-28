import json
from src.response.informational.kg.types_kg import KGContext
from src.response.informational.pipeline.state import InformationalState


def build_synthesis_input(
    kg_context: KGContext | None,
    rag_context: str | None,
) -> str:
    parts = []

    if kg_context is not None:
        parts.append("STRUCTURED ACADEMIC FACTS:\n" + json.dumps(kg_context, indent=2))

    if rag_context:
        parts.append("ACADEMIC RULES:\n" + rag_context)

    return "\n\n".join(parts)


def is_supported_informational_query(state: InformationalState) -> bool:
    # Enrollment eligibility
    if state.get("student_name") and state.get("subject_name"):
        return True

    # General academic rules (normative)
    if state.get("student_name") is None and state.get("subject_name") is None:
        return True

    return False