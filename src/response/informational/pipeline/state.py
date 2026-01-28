from typing import TypedDict, Optional
from src.response.informational.kg.types_kg import KGContext


class InformationalState(TypedDict):
    # --- input ---
    user_input: str

    # --- extracted entities ---
    student_name: Optional[str]
    subject_name: Optional[str]
    course_name: Optional[str]

    # --- knowledge ---
    kg_context: Optional[KGContext]
    rag_context: Optional[str]

    # --- output ---
    answer: Optional[str]