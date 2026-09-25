import os

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS


load_dotenv()


def get_embedding_model():
    """Create and return the Gemini embedding model."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")

    return GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=api_key
    )


def create_vector_store(chunks):
    """
    Create a FAISS vector store from PDF chunks.
    """

    embedding_model = get_embedding_model()

    texts = [chunk["text"] for chunk in chunks]

    metadatas = [
        {
            "page_number": chunk["page_number"]
        }
        for chunk in chunks
    ]

    vector_store = FAISS.from_texts(
        texts=texts,
        embedding=embedding_model,
        metadatas=metadatas
    )

    return vector_store


def search_vector_store(vector_store, question, k=3):
    """
    Retrieve the most relevant PDF chunks for a question.
    """

    results = vector_store.similarity_search(
        question,
        k=k
    )

    return results