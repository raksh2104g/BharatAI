from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.dependencies import get_current_user

from backend.app.models.user import User

from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.schemas.chat_history import ChatHistoryResponse

from backend.app.ai.llm_service import generate_answer
from backend.app.ai.rag_service import retrieve_context

from backend.app.services.chat_service import (
    save_chat,
    get_chat_history
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post(
    "",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Chat with BharatAI
    """

    # Retrieve relevant context
    contexts = retrieve_context(request.question)

    # Convert list to string
    context = "\n\n".join(contexts)

    # Generate AI answer
    answer = generate_answer(
        question=request.question,
        context=context
    )

    # Save chat history for logged-in user
    save_chat(
        db=db,
        user_id=current_user.id,
        question=request.question,
        answer=answer
    )

    return ChatResponse(
        answer=answer
    )


@router.get(
    "/history",
    response_model=List[ChatHistoryResponse]
)
def history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get chat history of logged-in user
    """

    return get_chat_history(
        db=db,
        user_id=current_user.id
    )