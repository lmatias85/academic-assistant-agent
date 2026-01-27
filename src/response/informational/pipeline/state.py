from typing import TypedDict
from src.response.informational.kg.types_kg import KGContext


class InformationalState(TypedDict):
    user_input: str
    kg_context: KGContext | None
    rag_context: str | None
    answer: str | None
