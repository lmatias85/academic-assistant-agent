from pathlib import Path


def load_rules_document(path: str) -> str:
    """
    Load the academic rules document as plain text.
    """
    return Path(path).read_text(encoding="utf-8")
