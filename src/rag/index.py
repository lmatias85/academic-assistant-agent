from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


def build_faiss_index(document_text: str) -> FAISS:
    """
    Build a FAISS vector index from the academic rules document.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    chunks = splitter.split_text(document_text)

    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_texts(chunks, embeddings)

    return vectorstore
