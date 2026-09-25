import os

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings


# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")


# Create embedding model
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=api_key
)


# Test text
text = "Supervised learning uses labelled data to train a model."


# Generate embedding
vector = embeddings.embed_query(text)


print("Embedding generated successfully!")
print("Vector length:", len(vector))
print("First 10 values:", vector[:10])

"""
This:

text = "Supervised learning uses labelled data to train a model."

went into:

Gemini Embedding Model
        ↓
[0.0123, -0.0456, 0.0789, ...]

That vector is the embedding.

Think of it as converting:

human-readable meaning → machine-readable numerical representation

Google describes embeddings as numerical representations that support similarity measurement and information retrieval.
"""