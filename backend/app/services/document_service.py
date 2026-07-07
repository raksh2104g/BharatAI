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
from backend.app.services.chunk_service import chunk_text

from backend.app.ai.embedding_service import generate_embedding
from backend.app.ai.vector_service import store_embeddings


UPLOAD_FOLDER = "backend/app/uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


def save_document(
    db: Session,
    file: UploadFile,
    user_id: int
):
    """
    Upload PDF, extract text,
    generate embeddings and
    store into PostgreSQL + Qdrant.
    """

    # ======================================
    # Save Uploaded File
    # ======================================

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # ======================================
    # Extract Text
    # ======================================

    extracted_text = extract_text_from_pdf(
        file_path
    )

    # ======================================
    # Split into Chunks
    # ======================================

    chunks = chunk_text(
        extracted_text
    )

    # ======================================
    # Generate Embeddings
    # ======================================

    embeddings = [
        generate_embedding(chunk)
        for chunk in chunks
    ]

    # ======================================
    # Save Metadata into PostgreSQL
    # ======================================

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

    # ======================================
    # Store Embeddings into Qdrant
    # ======================================

    store_embeddings(
        chunks=chunks,
        embeddings=embeddings,
        user_id=user_id,
        document_id=document.id,
        filename=document.filename
    )

    return document