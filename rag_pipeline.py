import os

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings


load_dotenv()


def get_embedding_model():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")

    return GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=api_key
    )


def create_embeddings(chunks):

    embeddings_model = get_embedding_model()

    texts = [chunk["text"] for chunk in chunks]

    vectors = embeddings_model.embed_documents(texts)

    return vectors