import json
from src.response.informational.kg.types_kg import KGContext


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
