from typing import TypedDict, Optional


class InformationalState(TypedDict):
    user_input: str

    # Outputs of individual nodes
    kg_context: Optional[str]
    rag_context: Optional[str]

    # Final answer
    answer: Optional[str]
