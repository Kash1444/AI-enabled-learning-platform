"""Learning material (trainer uploads) models."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, utcnow


class LearningMaterial(Base):
    """A file uploaded by a trainer and made available to the RAG pipeline."""

    __tablename__ = "learning_materials"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)  # mat_<uuid>
    title: Mapped[str] = mapped_column(String(250))
    original_filename: Mapped[str] = mapped_column(String(300))
    stored_filename: Mapped[str] = mapped_column(String(300))
    file_type: Mapped[str] = mapped_column(String(10))  # .pdf/.docx/.pptx/.txt
    competency_domain: Mapped[str] = mapped_column(String(80), default="")
    competency_skill: Mapped[str] = mapped_column(String(150), default="")
    uploaded_by: Mapped[str] = mapped_column(String(120), default="trainer")
    size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    chunk_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), default="processing")  # processing|ready|failed
    error_message: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class DocumentChunk(Base):
    """
    A text chunk extracted from a LearningMaterial. The chunk text is kept
    in SQL (source of truth / for citation display) while its embedding
    lives in the Chroma vector store, keyed by this row's `id`.
    """

    __tablename__ = "document_chunks"

    id: Mapped[str] = mapped_column(String(60), primary_key=True)  # chunk_<uuid>
    material_id: Mapped[str] = mapped_column(String(40), index=True)
    chunk_index: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
