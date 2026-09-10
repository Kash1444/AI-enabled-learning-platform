"""Pydantic schemas for the AI learning assistant."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    employee_id: str
    message: str = Field(..., min_length=1, max_length=2000)
    material_id: Optional[str] = Field(
        None, description="If set, the assistant answers using RAG over this material only."
    )


class SourceRef(BaseModel):
    material_id: str
    material_title: str
    chunk_id: str
    text_preview: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceRef] = Field(default_factory=list)
    used_rag: bool
    mode: str  # "rag" | "profile" | "general"
