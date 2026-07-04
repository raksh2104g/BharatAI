"""
========================================
Project : BharatAI
Module  : LLM Service
Purpose : Generate AI Answers using Groq
========================================
"""

from groq import Groq

from backend.app.config import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


def generate_answer(
    question: str,
    context: str
):
    """
    Generate answer using Groq LLM.
    """

    prompt = f"""
You are BharatAI.

Answer ONLY using the provided context.

If the answer is not present,
reply:

"I could not find the answer in the document."

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content