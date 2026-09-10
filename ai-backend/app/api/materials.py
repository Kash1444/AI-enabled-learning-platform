"""Learning material upload & retrieval endpoints (trainer flow)."""

from __future__ import annotations

import logging
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import (
    resolve_within_upload_dir,
    safe_filename,
    validate_upload_extension,
    validate_upload_size,
)
from app.models.material import DocumentChunk, LearningMaterial
from app.processors.document_processor import chunk_text, clean_text, extract_text
from app.schemas.material import (
    MaterialChunkPreview,
    MaterialDetailResponse,
    MaterialListResponse,
    MaterialResponse,
)

logger = logging.getLogger(__name__)
settings = get_settings()
router = APIRouter(prefix="/api/materials", tags=["Materials"])


@router.post(
    "/upload",
    response_model=MaterialResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a learning material for RAG-based MCQ generation",
    description=(
        "Accepts PDF, DOCX, PPTX or TXT files. The file is validated, stored safely, text is "
        "extracted/cleaned/chunked, embeddings are generated and stored in the vector index, "
        "and the material becomes available to the assessment generator and AI assistant."
    ),
)
async def upload_material(
    file: UploadFile = File(...),
    title: str = Form(...),
    competency_domain: str = Form(""),
    competency_skill: str = Form(""),
    uploaded_by: str = Form("trainer"),
    db: Session = Depends(get_db),
) -> MaterialResponse:
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No filename provided.")

    ext = validate_upload_extension(file.filename)
    contents = await file.read()
    validate_upload_size(len(contents))

    stored_name = safe_filename(file.filename)
    dest_path = resolve_within_upload_dir(stored_name)
    dest_path.write_bytes(contents)

    material_id = f"mat_{uuid.uuid4().hex[:12]}"
    material = LearningMaterial(
        id=material_id,
        title=title or file.filename,
        original_filename=file.filename,
        stored_filename=stored_name,
        file_type=ext,
        competency_domain=competency_domain,
        competency_skill=competency_skill,
        uploaded_by=uploaded_by,
        size_bytes=len(contents),
        chunk_count=0,
        status="processing",
    )
    db.add(material)
    db.commit()
    db.refresh(material)

    try:
        raw_text = extract_text(dest_path, ext)
        cleaned = clean_text(raw_text)
        if not cleaned:
            raise ValueError("No extractable text found in the uploaded file.")
        chunks = chunk_text(cleaned)
        if not chunks:
            raise ValueError("Text extraction succeeded but produced no chunks.")

        chunk_rows = []
        for i, chunk in enumerate(chunks):
            chunk_id = f"chunk_{uuid.uuid4().hex[:12]}"
            db.add(DocumentChunk(id=chunk_id, material_id=material_id, chunk_index=i, text=chunk))
            chunk_rows.append({"chunk_id": chunk_id, "text": chunk})
        db.commit()

        # Index into the vector store (best-effort - never blocks the upload response on failure).
        try:
            from app.ai.rag import get_rag_pipeline

            get_rag_pipeline().index_material(material_id, chunk_rows)
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "Vector indexing failed for material %s (will still work via SQL fallback): %s",
                material_id,
                exc,
            )

        material.chunk_count = len(chunk_rows)
        material.status = "ready"
        db.commit()
        db.refresh(material)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to process uploaded material %s", material_id)
        material.status = "failed"
        material.error_message = str(exc)[:500]
        db.commit()
        db.refresh(material)

    return MaterialResponse.model_validate(material)


@router.get(
    "",
    response_model=MaterialListResponse,
    summary="List all uploaded learning materials",
)
def list_materials(db: Session = Depends(get_db)) -> MaterialListResponse:
    materials = db.query(LearningMaterial).order_by(LearningMaterial.created_at.desc()).all()
    return MaterialListResponse(materials=[MaterialResponse.model_validate(m) for m in materials])


@router.get(
    "/{material_id}",
    response_model=MaterialDetailResponse,
    summary="Get a single learning material, including a preview of its chunks",
)
def get_material(material_id: str, db: Session = Depends(get_db)) -> MaterialDetailResponse:
    material = db.query(LearningMaterial).filter(LearningMaterial.id == material_id).first()
    if not material:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Material '{material_id}' not found.")

    chunks = (
        db.query(DocumentChunk)
        .filter(DocumentChunk.material_id == material_id)
        .order_by(DocumentChunk.chunk_index)
        .limit(10)
        .all()
    )
    chunk_previews = [
        MaterialChunkPreview(
            chunk_id=c.id,
            chunk_index=c.chunk_index,
            text_preview=(c.text[:200] + ("..." if len(c.text) > 200 else "")),
        )
        for c in chunks
    ]
    payload = MaterialDetailResponse.model_validate(material)
    payload.chunks = chunk_previews
    return payload
