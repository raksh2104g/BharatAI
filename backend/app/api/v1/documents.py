"""
========================================
Project : BharatAI
Module  : Document API
Purpose : Upload Documents
========================================
"""

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.dependencies import get_current_user

from backend.app.models.user import User
from backend.app.schemas.document import DocumentResponse
from backend.app.services.document_service import save_document


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post(
    "/upload",
    response_model=DocumentResponse
)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = save_document(
        db=db,
        file=file,
        user_id=current_user.id
    )

    return document