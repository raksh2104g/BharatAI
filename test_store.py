from backend.app.ai.embedding_service import generate_embedding
from backend.app.ai.vector_service import (
    client,
    COLLECTION_NAME,
    store_embeddings
)

chunks = [
    "Internship duration is 6 weeks.",
    "Stipend is ₹15,000 per month."
]

embeddings = [
    generate_embedding(chunk)
    for chunk in chunks
]

store_embeddings(
    chunks,
    embeddings
)

count = client.count(
    collection_name=COLLECTION_NAME
)

print("Total vectors:", count.count)