import json
from src.response.informational.pipeline.state import InformationalState
from src.response.informational.entities.types_entities import InformationalEntities
from src.response.informational.entities.prompt import INFORMATIONAL_ENTITY_PROMPT
from src.response.agent.llm_client import call_llm


def extract_entities_node(
    state: InformationalState,
) -> InformationalState:
    user_input = state["user_input"]

    response = call_llm(
        system_prompt=INFORMATIONAL_ENTITY_PROMPT,
        user_prompt=user_input,
        temperature=0,
    )

    parsed = json.loads(response)
    entities = InformationalEntities(**parsed)

    state["student_name"] = entities.student_name
    state["subject_name"] = entities.subject_name

    return state
