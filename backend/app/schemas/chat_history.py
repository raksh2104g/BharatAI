"""
========================================
Project : BharatAI
Module  : Chat History Schema
Purpose : Request & Response Models
========================================
"""

from datetime import datetime

from pydantic import BaseModel


class ChatHistoryResponse(BaseModel):
    id: int
    user_id: int
    question: str
    answer: str
    created_at: datetime

    class Config:
        from_attributes = True