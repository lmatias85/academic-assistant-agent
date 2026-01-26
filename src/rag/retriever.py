from langchain_community.vectorstores import FAISS


def retrieve_rules_context(vectorstore: FAISS, query: str, k: int = 3) -> str:
    """
    Retrieve relevant academic rules for a given query.
    """
    docs = vectorstore.similarity_search(query, k=k)

    return "\n".join(doc.page_content for doc in docs)
