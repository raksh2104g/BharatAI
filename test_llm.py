from backend.app.ai.llm_service import generate_answer


context = """
Internship duration is 6 weeks.
Stipend is ₹15000 per month.
"""

question = "What is internship duration?"


answer = generate_answer(
    question,
    context
)

print(answer)