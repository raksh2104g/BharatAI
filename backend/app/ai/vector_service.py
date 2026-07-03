"""
========================================
Project : BharatAI
Module  : Vector Service
Purpose : Store & Search Embeddings
========================================
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(":memory:")

COLLECTION_NAME = "documents"

# Create collection if not exists
collections = [c.name for c in client.get_collections().collections]

if COLLECTION_NAME not in collections:
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )