import json
from src.response.agent.llm_client import call_llm
from src.response.agent.agent_utils import extract_json
from src.response.informational.entities.types_entities import AcademicEntities
from src.response.informational.entities.normalize import normalize_academic_entities
from src.response.informational.entities.prompt import ACADEMIC_ENTITY_PROMPT
from src.response.informational.kg.context import build_kg_context
from src.response.informational.pipeline.state import InformationalState
from src.response.informational.pipeline.utlis import (
    build_synthesis_input,
    is_supported_informational_query,
)
from src.response.informational.pipeline.prompt import SYNTHESIS_SYSTEM_PROMPT
from src.response.informational.rag import get_rules_vectorstore
from src.response.informational.rag.retriever import retrieve_rules_context


def extract_entities_node(
    state: InformationalState,
) -> InformationalState:
    user_input = state["user_input"]

    response = call_llm(
        system_prompt=ACADEMIC_ENTITY_PROMPT,
        user_prompt=user_input,
        temperature=0,
    )

    parsed = json.loads(extract_json(response))
    entities = AcademicEntities(**parsed)

    state["student_name"] = entities.student_name
    state["subject_name"] = entities.subject_name
    state["course_name"] = entities.course_name

    normalize_academic_entities(state)

    if not entities.is_academic():
        state["answer"] = (
            "This question does not appear to be related to the academic system."
        )
        return state

    if entities.is_academic() and not is_supported_informational_query(state):
        state["answer"] = "This academic question is not supported yet by the system."
        return state

    return state


def kg_query_node(state: InformationalState) -> InformationalState:

    if state.get("answer") is not None:
        return state

    student_name = str(state.get("student_name"))
    subject_name = str(state.get("subject_name"))

    if not student_name or not subject_name:
        state["kg_context"] = None
        return state

    state["kg_context"] = build_kg_context(student_name, subject_name)
    return state


def rag_retrieval_node(state: InformationalState) -> InformationalState:
    """
    Retrieve relevant academic rules using RAG (FAISS).
    """
    if state.get("answer") is not None:
        return state

    vectorstore = get_rules_vectorstore()

    user_query = state["user_input"]
    rules_context = retrieve_rules_context(vectorstore, user_query)

    state["rag_context"] = rules_context

    return state


def synthesis_node(state: InformationalState) -> InformationalState:

    if state.get("answer") is not None:
        return state

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
