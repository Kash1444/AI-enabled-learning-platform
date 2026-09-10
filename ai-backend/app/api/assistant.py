"""AI Learning Assistant endpoint."""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.assistant import ChatRequest, ChatResponse
from app.services import assistant_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/assistant", tags=["Assistant"])


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with the AI learning assistant",
    description=(
        "If `material_id` is provided, the assistant retrieves relevant chunks from that "
        "material (RAG) and grounds its answer in them, returning citations. If the message "
        "looks like a question about the learner's own competency/skill-gap profile, it is "
        "answered directly from the deterministic engines. Otherwise a general, "
        "clearly-scoped answer is given."
    ),
)
def chat(payload: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    try:
        return assistant_service.chat(
            db, employee_id=payload.employee_id, message=payload.message, material_id=payload.material_id
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Assistant chat failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="The AI assistant could not respond."
        ) from exc
