"""
========================================
Project : BharatAI
Module  : RAG Service
Purpose : Retrieve Relevant Chunks
========================================
"""

from typing import List, Dict

from backend.app.ai.embedding_service import generate_embedding
from backend.app.ai.vector_service import search_embeddings


def retrieve_context(
    question: str,
    user_id: int,
    limit: int = 3
) -> List[Dict]:
    """
    Retrieve relevant chunks with metadata
    from the current user's documents.
    """

    # Generate embedding for the question
    question_embedding = generate_embedding(
        question
    )

    # Search relevant chunks
    results = search_embeddings(
        embedding=question_embedding,
        user_id=user_id,
        limit=limit
    )

    contexts: List[Dict] = []

    for point in results:

        payload = point.payload or {}

        contexts.append(
            {
                "text": payload.get("text", ""),
                "filename": payload.get("filename", ""),
                "document_id": payload.get("document_id"),
                "user_id": payload.get("user_id")
            }
        )

    return contexts