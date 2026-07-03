"""
========================================
Project : BharatAI
Module  : Embedding Service
Purpose : Generate Embeddings
========================================
"""

from sentence_transformers import SentenceTransformer

# Load Model Only Once
model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


def generate_embedding(text: str):

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()