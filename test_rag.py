from backend.app.ai.rag_service import retrieve_context

question = "What is internship duration?"

contexts = retrieve_context(question)

print("\nRetrieved Contexts:\n")

for i, context in enumerate(contexts, start=1):
    print(f"{i}. {context}")
    print("-" * 50)