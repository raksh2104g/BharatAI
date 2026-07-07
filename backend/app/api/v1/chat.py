"""
========================================
Project : BharatAI
Module  : Chat API
Purpose : AI Chat + Chat History
========================================
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.dependencies import get_current_user

from backend.app.models.user import User

from backend.app.schemas.chat import (
    ChatRequest,
    ChatResponse
)

from backend.app.schemas.chat_history import (
    ChatHistoryResponse
)

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

    # ======================================
    # Retrieve Relevant Context
    # ======================================

    contexts = retrieve_context(
        question=request.question,
        user_id=current_user.id
    )

    # ======================================
    # Build Context for LLM
    # ======================================

    context = "\n\n".join(
        item["text"]
        for item in contexts
    )

    # ======================================
    # Generate AI Answer
    # ======================================

    answer = generate_answer(
        question=request.question,
        context=context
    )

    # ======================================
    # Collect Source Documents
    # ======================================

    sources: List[str] = []

    for item in contexts:

        filename = item.get("filename")

        if (
            filename
            and filename not in sources
        ):
            sources.append(filename)

    # ======================================
    # Save Chat History
    # ======================================

    save_chat(
        db=db,
        user_id=current_user.id,
        question=request.question,
        answer=answer
    )

    # ======================================
    # Return Response
    # ======================================

    return ChatResponse(
        answer=answer,
        sources=sources
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
    Get chat history
    of current logged-in user.
    """

    return get_chat_history(
        db=db,
        user_id=current_user.id
    )