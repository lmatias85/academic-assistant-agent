import re


def extract_json(text: str) -> str:
    """
    Extracts a JSON object from an LLM response.
    Handles fenced code blocks like ```json ... ```
    """
    text = text.strip()

    # Remove ```json or ``` wrappers
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text)
        text = re.sub(r"```$", "", text)

    return text.strip()