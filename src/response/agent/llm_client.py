from openai import OpenAI

_client = OpenAI()


def call_llm(
    *,
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0,
) -> str:
    response = _client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
    )

    content = response.choices[0].message.content
    if content is None:
        raise RuntimeError("LLM returned empty response")

    return content
