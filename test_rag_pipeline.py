from backend.app.ai.embedding_service import generate_embedding
from backend.app.ai.vector_service import (
    store_embeddings,
    search_embeddings
)

# Sample chunks
chunks = [
    "Internship duration is 6 weeks.",
    "Stipend is ₹15000 per month."
]

print("Generating embeddings...")

embeddings = [
    generate_embedding(chunk)
    for chunk in chunks
]

print("Storing embeddings...")

store_embeddings(
    chunks,
    embeddings
)

print("Searching...")

question = "What is internship duration?"

question_embedding = generate_embedding(question)

results = search_embeddings(question_embedding)

print("\nRESULTS\n")

for point in results:
    print(point.payload)