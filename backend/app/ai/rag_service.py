"""
========================================
Project : BharatAI
Module  : RAG Service
Purpose : Retrieve Relevant Chunks
========================================
"""

from backend.app.ai.embedding_service import generate_embedding
from backend.app.ai.vector_service import search_embeddings


def retrieve_context(
    question: str,
    limit: int = 3
):
    """
    Retrieve relevant chunks from Qdrant.
    """

    question_embedding = generate_embedding(question)

    results = search_embeddings(
        question_embedding,
        limit
    )

    contexts = []

    for point in results:
        contexts.append(
            point.payload["text"]
        )

    return contexts