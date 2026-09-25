import os

from dotenv import load_dotenv

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)

from langchain_community.vectorstores import FAISS


load_dotenv()


# --------------------------------------------------
# GEMINI EMBEDDINGS
# --------------------------------------------------

def get_embedding_model():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found in .env file"
        )

    return GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=api_key
    )


# --------------------------------------------------
# CREATE FAISS VECTOR STORE
# --------------------------------------------------

def create_vector_store(chunks):

    embedding_model = get_embedding_model()

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

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


# --------------------------------------------------
# SEMANTIC SEARCH
# --------------------------------------------------

def search_vector_store(
    vector_store,
    question,
    k=3
):

    results = vector_store.similarity_search(
        question,
        k=k
    )

    return results


# --------------------------------------------------
# GEMINI LLM
# --------------------------------------------------

def generate_answer(
    question,
    retrieved_chunks
):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found in .env file"
        )

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=api_key,
        temperature=0
    )

    context_parts = []

    for chunk in retrieved_chunks:

        page_number = chunk.metadata.get(
            "page_number",
            "Unknown"
        )

        context_parts.append(
            f"Page {page_number}:\n"
            f"{chunk.page_content}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the
information contained in the document context.

Do not use outside knowledge.

If the answer cannot be found in the
provided context, say:

"I could not find the answer in the uploaded document."

DOCUMENT CONTEXT:
-----------------
{context}
-----------------

USER QUESTION:
{question}

ANSWER:
"""

    response = llm.invoke(prompt)

    return response.content