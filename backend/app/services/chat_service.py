"""
========================================
Project : BharatAI
Module  : Chat Service
Purpose : Save & Fetch Chat History
========================================
"""

from sqlalchemy.orm import Session

from backend.app.models.chat import Chat


def save_chat(
    db: Session,
    user_id: int,
    question: str,
    answer: str
):
    chat = Chat(
        user_id=user_id,
        question=question,
        answer=answer
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat


def get_chat_history(
    db: Session,
    user_id: int
):
    return (
        db.query(Chat)
        .filter(Chat.user_id == user_id)
        .order_by(Chat.created_at.desc())
        .all()
    )