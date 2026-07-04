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


def store_embeddings(chunks, embeddings):
    """
    Store embeddings into Qdrant.
    """

    points = []

    for chunk, embedding in zip(chunks, embeddings):
        points.append(
            PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload={
                    "text": chunk
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )


from qdrant_client.models import Filter


def search_embeddings(
    embedding,
    limit: int = 3
):
    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=embedding,
        limit=limit,
        with_payload=True
    )

    return response.points