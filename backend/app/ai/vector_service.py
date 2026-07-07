"""
========================================
Project : BharatAI
Module  : Vector Service
Purpose : Store & Search Embeddings
========================================
"""

from uuid import uuid4
from typing import List

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)

# ======================================================
# Docker Qdrant Connection
# ======================================================

client = QdrantClient(
    url="http://localhost:6333"
)

COLLECTION_NAME = "documents"

# ======================================================
# Create Collection (Only Once)
# ======================================================

try:

    collections = [
        collection.name
        for collection in client.get_collections().collections
    ]

    if COLLECTION_NAME not in collections:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

        print(f"✅ Collection '{COLLECTION_NAME}' created.")

    else:

        print(f"✅ Collection '{COLLECTION_NAME}' already exists.")

except Exception as e:

    print(f"❌ Qdrant Connection Error: {e}")


# ======================================================
# Store Embeddings
# ======================================================

def store_embeddings(
    chunks: List[str],
    embeddings: List[List[float]],
    user_id: int,
    document_id: int,
    filename: str
):
    """
    Store document embeddings in Qdrant.
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

    print(f"✅ Stored {len(points)} embeddings.")


# ======================================================
# Search Embeddings
# ======================================================

def search_embeddings(
    embedding: List[float],
    user_id: int,
    limit: int = 3
):
    """
    Search embeddings only from
    current logged-in user's documents.
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