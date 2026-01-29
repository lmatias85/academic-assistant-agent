from src.response.informational.rag.loader import load_rules_document
from src.response.informational.rag.index import build_faiss_index

_RULES_PATH = "data/documentation/Academic_Rules_School_EN.md"

_rules_text = load_rules_document(_RULES_PATH)
_vectorstore = build_faiss_index(_rules_text)


def get_rules_vectorstore():
    return _vectorstore
