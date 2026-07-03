from backend.app.ai.embedding_service import generate_embedding

text = "Your internship duration is 6 weeks."

embedding = generate_embedding(text)

print(type(embedding))
print(len(embedding))
print(embedding[:10])