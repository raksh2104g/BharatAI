from backend.app.ai.embedding_service import generate_embedding
from backend.app.ai.vector_service import (
    search_embeddings,
)

question = "How long is the internship?"

embedding = generate_embedding(question)

results = search_embeddings(embedding)

for item in results:
    print(item.payload["text"])