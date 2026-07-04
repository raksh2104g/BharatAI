"""
=========================================
Project : BharatAI
Module  : Main API Router
Purpose : Connects all API Routes
=========================================
"""

from fastapi import APIRouter

from backend.app.api.v1.health import router as health_router
from backend.app.api.v1.users import router as user_router
from backend.app.api.v1.documents import router as document_router
from backend.app.api.v1.chat import router as chat_router


# Main Router
router = APIRouter()

# Include Health Routes
router.include_router(health_router)

# Include User Routes
router.include_router(user_router)

# Include Document Routes
router.include_router(document_router)

router.include_router(chat_router)