import json

from openai import OpenAI
from pydantic import ValidationError
from src.agent.types import AgentDecision, LLMDecision
from src.agent.prompts import SYSTEM_PROMPT


class PrimaryAgent:
    """
    Primary decision agent powered by an LLM.

    Responsible for:
    - deciding the route (informational vs action)
    - extracting structured arguments for actions (when applicable)
    """

    def __init__(self) -> None:
        self.client = OpenAI()

    def decide(self, user_input: str) -> AgentDecision:

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input},
            ],
            temperature=0,
        )

        content = response.choices[0].message.content

        if content is None:
            raise RuntimeError("LLM response content is None; cannot parse decision.")

        try:
            parsed = json.loads(content)
            llm_decision = LLMDecision(**parsed)
        except (json.JSONDecodeError, ValidationError) as exc:
            raise RuntimeError(
                f"Failed to parse LLM decision output: {content}"
            ) from exc

        # Propagate arguments only if present and validated
        arguments = (
            llm_decision.arguments.model_dump()
            if llm_decision.arguments is not None
            else None
        )

        return AgentDecision(
            route=llm_decision.route,
            reason=llm_decision.reason,
            arguments=arguments,
        )
