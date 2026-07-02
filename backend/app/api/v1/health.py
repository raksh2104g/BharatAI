"""
=========================================
Project : BharatAI
Module  : Health API
Purpose : Health and Version Endpoints
=========================================
"""

from fastapi import APIRouter
from backend.app.config import settings

# Create Router
router = APIRouter()


# ==========================================
# Health Check API
# URL : /health
# ==========================================
@router.get("/health")
def health():
    return {
        "status": "healthy",
        "message": "BharatAI Backend is running"
    }


# ==========================================
# Version API
# URL : /version
# ==========================================
@router.get("/version")
def version():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }