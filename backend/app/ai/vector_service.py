"""
========================================
Project : BharatAI
Module  : Vector Service
Purpose : Store & Search Embeddings
========================================
"""

from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)

client = QdrantClient(path="backend/qdrant_data")

COLLECTION_NAME = "documents"

collections = [
    c.name
    for c in client.get_collections().collections
]

if COLLECTION_NAME not in collections:
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )


def store_embeddings(
    chunks,
    embeddings,
    user_id: int,
    document_id: int,
    filename: str
):
    """
    Store embeddings with metadata.
    """

    points = []

    for chunk, embedding in zip(chunks, embeddings):

        points.append(
            PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "user_id": user_id,
                    "document_id": document_id,
                    "filename": filename
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )


def search_embeddings(
    embedding,
    user_id: int,
    limit: int = 3
):
    """
    Search only current user's documents.
    """

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=embedding,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=user_id)
                )
            ]
        ),
        limit=limit,
        with_payload=True
    )

    return response.points



