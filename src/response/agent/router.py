import json

from openai import OpenAI
from pydantic import ValidationError
from response.agent.types_agent import RouterDecision, LLMDecision
from src.response.agent.prompts import SYSTEM_PROMPT


class RouterAgent:
    """
    Primary decision agent powered by an LLM.

    Responsible for:
    - deciding the route (informational vs action)
    - extracting structured arguments for actions (when applicable)
    """

    def __init__(self) -> None:
        self.client = OpenAI()

    def decide(self, user_input: str) -> RouterDecision:

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

        parsed = json.loads(content)
        llm_decision = LLMDecision(**parsed)

        return RouterDecision(
            route=llm_decision.route,
            reason=llm_decision.reason,
            tool_name=llm_decision.tool_name,
            arguments=llm_decision.arguments,
        )
