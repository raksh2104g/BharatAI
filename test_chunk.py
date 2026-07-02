from backend.app.services.chunk_service import chunk_text

text = "Hello BharatAI " * 200

chunks = chunk_text(text)

print("Total Chunks:", len(chunks))

print()

print(chunks[0])