"""
========================================
Project : BharatAI
Module  : Document Service
Purpose : Upload Document Logic
========================================
"""

import os
import shutil

from fastapi import UploadFile
from sqlalchemy.orm import Session

from backend.app.models.document import Document
from backend.app.services.pdf_service import extract_text_from_pdf


UPLOAD_FOLDER = "backend/app/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def save_document(
    db: Session,
    file: UploadFile,
    user_id: int
):
    # File Save Path
    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    # Save File
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )


    # Extract PDF Text
    extracted_text = extract_text_from_pdf(file_path)    

    # Database Object
    document = Document(
    filename=file.filename,
    filepath=file_path,
    filetype=file.content_type,
    filesize=os.path.getsize(file_path),
    uploaded_by=user_id,
    extracted_text=extracted_text
)

    db.add(document)
    db.commit()
    db.refresh(document)

    return document