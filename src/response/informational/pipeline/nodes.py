import json
from src.response.agent.llm_client import call_llm
from src.response.informational.entities.types_entities import InformationalEntities
from src.response.informational.entities.prompt import INFORMATIONAL_ENTITY_PROMPT
from src.response.informational.kg.context import build_kg_context
from src.response.informational.pipeline.state import InformationalState
from src.response.informational.pipeline.utlis import build_synthesis_input
from src.response.informational.pipeline.prompt import SYNTHESIS_SYSTEM_PROMPT
from src.response.informational.rag import get_rules_vectorstore
from src.response.informational.rag.retriever import retrieve_rules_context


def reasoning_node(state: InformationalState) -> InformationalState:
    """
    Initial reasoning node.
    For now, it simply passes the user input forward.
    """
    return state


def extract_entities_node(
    state: InformationalState,
) -> InformationalState:
    user_input = state["user_input"]

    response = call_llm(
        system_prompt=INFORMATIONAL_ENTITY_PROMPT,
        user_prompt=user_input,
        temperature=0,
    )

    print("[Entity Extraction] Raw LLM response:", response)

    parsed = json.loads(response)
    entities = InformationalEntities(**parsed)

    state["student_name"] = entities.student_name
    state["subject_name"] = entities.subject_name

    return state


def kg_query_node(state: InformationalState) -> InformationalState:
    student_name = str(state.get("student_name"))
    subject_name = str(state.get("subject_name"))

    if student_name and subject_name:
        state["kg_context"] = build_kg_context(
            student_name=student_name,
            subject_name=subject_name,
        )
    else:
        state["kg_context"] = None

    return state


def rag_retrieval_node(state: InformationalState) -> InformationalState:
    """
    Retrieve relevant academic rules using RAG (FAISS).
    """
    vectorstore = get_rules_vectorstore()

    user_query = state["user_input"]
    rules_context = retrieve_rules_context(vectorstore, user_query)

    state["rag_context"] = rules_context
    return state


def synthesis_node(state: InformationalState) -> InformationalState:
    kg_context = state.get("kg_context")
    rag_context = state.get("rag_context")

    # --- Case 1: nothing useful ---
    if kg_context is None and not rag_context:
        state["answer"] = (
            "I need more information to answer your question precisely. "
            "Please provide additional details."
        )
        return state

    synthesis_input = build_synthesis_input(
        kg_context=kg_context,
        rag_context=rag_context,
    )

    response = call_llm(
        system_prompt=SYNTHESIS_SYSTEM_PROMPT,
        user_prompt=synthesis_input,
        temperature=0,
    )

    state["answer"] = response
    return state
