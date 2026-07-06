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
    user_id: int,
    limit: int = 3
):
    """
    Retrieve relevant chunks
    only from current user's documents.
    """

    question_embedding = generate_embedding(question)

    results = search_embeddings(
        embedding=question_embedding,
        user_id=user_id,
        limit=limit
    )

    contexts = []

    for point in results:
        contexts.append(
            point.payload["text"]
        )

    return contexts