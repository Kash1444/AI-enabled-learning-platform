"""Pydantic schemas for learning-material upload & retrieval."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class MaterialResponse(BaseModel):
    id: str
    title: str
    original_filename: str
    file_type: str
    competency_domain: str
    competency_skill: str
    uploaded_by: str
    size_bytes: int
    chunk_count: int
    status: str
    error_message: str = ""
    created_at: datetime

    model_config = {"from_attributes": True}


class MaterialListResponse(BaseModel):
    materials: List[MaterialResponse]


class MaterialChunkPreview(BaseModel):
    chunk_id: str
    chunk_index: int
    text_preview: str


class MaterialDetailResponse(MaterialResponse):
    chunks: Optional[List[MaterialChunkPreview]] = None
