from fastapi import APIRouter

from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.ai.llm_service import generate_answer
from backend.app.ai.rag_service import retrieve_context

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post(
    "",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    # Retrieve relevant chunks
    contexts = retrieve_context(
        request.question
    )

    # Convert list into single string
    context = "\n\n".join(contexts)

    # Generate final answer
    answer = generate_answer(
        question=request.question,
        context=context
    )

    return ChatResponse(
        answer=answer
    )