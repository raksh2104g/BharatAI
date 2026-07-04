from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.ai.llm_service import generate_answer
from backend.app.ai.rag_service import retrieve_context
from backend.app.services.chat_service import save_chat

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
    db: Session = Depends(get_db)
):

    # Temporary user
    user_id = 1

    # Retrieve Context
    contexts = retrieve_context(request.question)

    context = "\n\n".join(contexts)

    # Generate Answer
    answer = generate_answer(
        question=request.question,
        context=context
    )

    # Save Chat
    save_chat(
        db=db,
        user_id=user_id,
        question=request.question,
        answer=answer
    )

    return ChatResponse(
        answer=answer
    )



from typing import List
from backend.app.schemas.chat_history import ChatHistoryResponse
from backend.app.services.chat_service import get_chat_history


@router.get(
    "/history",
    response_model=List[ChatHistoryResponse]
)
def history(
    db: Session = Depends(get_db)
):

    # Temporary user
    user_id = 1

    return get_chat_history(
        db=db,
        user_id=user_id
    )