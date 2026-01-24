import json

from openai import OpenAI
from pydantic import ValidationError
from src.agent.types import AgentDecision, Route, LLMDecision
from src.agent.prompts import SYSTEM_PROMPT


class PrimaryAgent:
    """
    Primary decision agent.

    Responsible only for deciding whether a user request
    is informational or action-oriented.
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
            raise RuntimeError(
                "LLM response content is None; cannot parse decision."
            )

        try:
            parsed = json.loads(content)
            decision = LLMDecision(**parsed)
        except (json.JSONDecodeError, ValidationError) as exc:
            raise RuntimeError(
                f"Failed to parse LLM decision output: {content}"
            ) from exc


        return AgentDecision(
            route=decision.route,
            reason=decision.reason,
        )
