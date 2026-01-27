import json

from pydantic import ValidationError

from response.agent.llm_client import call_llm
from response.agent.types_agent import RouterDecision, LLMDecision
from response.agent.prompts import SYSTEM_PROMPT


class RouterAgent:
    """
    Primary decision agent powered by an LLM.

    Responsible for:
    - deciding the route (informational vs action)
    - extracting structured arguments for actions (when applicable)
    """

    def decide(self, user_input: str) -> RouterDecision:
        content = call_llm(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_input,
            temperature=0,
        )

        try:
            parsed = json.loads(content)
            llm_decision = LLMDecision(**parsed)
        except (json.JSONDecodeError, ValidationError) as exc:
            raise RuntimeError(
                f"Failed to parse LLM decision output: {content}"
            ) from exc

        return RouterDecision(
            route=llm_decision.route,
            reason=llm_decision.reason,
            tool_name=llm_decision.tool_name,
            arguments=llm_decision.arguments,
        )
