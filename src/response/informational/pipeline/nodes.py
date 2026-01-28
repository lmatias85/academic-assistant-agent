import json
from src.response.informational.pipeline.state import InformationalState
from src.response.informational.kg.context import build_kg_context
from src.response.informational.rag import get_rules_vectorstore
from src.response.informational.rag.retriever import retrieve_rules_context
from src.response.informational.entities.types_entities import InformationalEntities
from src.response.informational.entities.prompt import INFORMATIONAL_ENTITY_PROMPT
from src.response.agent.llm_client import call_llm


def reasoning_node(state: InformationalState) -> InformationalState:
    """
    Initial reasoning node.
    For now, it simply passes the user input forward.
    """
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

    if kg_context is None:
        state["answer"] = (
            "I need more information to answer your question precisely. "
            "Please specify the student and the subject you are referring to."
        )
        return state

    enrollment_eval = kg_context["evaluations"]["enrollment_eligibility"]
    student = kg_context["entities"]["student"]["name"]
    subject = kg_context["entities"]["subject"]["name"]

    if enrollment_eval["eligible"]:
        conclusion = f"{student} is eligible to enroll in {subject}."
    else:
        reasons = "; ".join(enrollment_eval["reasons"])
        conclusion = (
            f"{student} is not eligible to enroll in {subject}. "
            f"Reason(s): {reasons}."
        )

    if rag_context:
        state["answer"] = (
            f"{conclusion}\n\n" f"According to the academic rules:\n{rag_context}"
        )
    else:
        state["answer"] = conclusion

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
