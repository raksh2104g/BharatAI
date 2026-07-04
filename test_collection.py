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

# Temporary In-Memory Database
client = QdrantClient(":memory:")

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


def search_embeddings(
    embedding,
    limit=3
):
    result = client.query_points(
        collection_name=COLLECTION_NAME,
        query=embedding,
        limit=limit
    )

    return result.points