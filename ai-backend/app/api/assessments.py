"""Assessment generation, retrieval and evaluation endpoints."""

from __future__ import annotations

import json
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.assessment import Assessment
from app.schemas.assessment import (
    AssessmentResponse,
    AssessmentResponseForLearner,
    EvaluateAssessmentRequest,
    EvaluateAssessmentResponse,
    GenerateAssessmentRequest,
    QuestionOut,
    QuestionOutForLearner,
)
from app.services import assessment_engine

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/assessment", tags=["Assessment"])


@router.post(
    "/generate",
    response_model=AssessmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate an MCQ assessment",
    description=(
        "If `material_id` is supplied, questions are generated via RAG retrieval over that "
        "uploaded material and are strictly grounded in it (no hallucinated facts). If "
        "`material_id` is omitted, a generic, catalog-derived competency self-check is "
        "generated instead. Works fully offline in DEMO_MODE."
    ),
)
def generate_assessment(payload: GenerateAssessmentRequest, db: Session = Depends(get_db)) -> AssessmentResponse:
    try:
        assessment = assessment_engine.generate_assessment(
            db,
            material_id=payload.material_id,
            competency=payload.competency,
            domain=payload.domain,
            num_questions=payload.num_questions,
            difficulty=payload.difficulty,
            employee_id=payload.employee_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        logger.exception("Assessment generation failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate assessment."
        ) from exc

    return AssessmentResponse(
        id=assessment.id,
        title=assessment.title,
        competency_domain=assessment.competency_domain,
        competency_skill=assessment.competency_skill,
        difficulty=assessment.difficulty,
        material_id=assessment.material_id,
        generated_by=assessment.generated_by,
        created_at=assessment.created_at,
        questions=[
            QuestionOut(
                id=q.id,
                question=q.question,
                options=json.loads(q.options),
                correct_answer=q.correct_answer,
                explanation=q.explanation,
                competency=q.competency,
                difficulty=q.difficulty,
                source=q.source,
            )
            for q in assessment.questions
        ],
    )


@router.get(
    "/{assessment_id}",
    response_model=AssessmentResponseForLearner,
    summary="Get an assessment for a learner to attempt (no answer key included)",
)
def get_assessment(assessment_id: str, db: Session = Depends(get_db)) -> AssessmentResponseForLearner:
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Assessment '{assessment_id}' not found."
        )
    return AssessmentResponseForLearner(
        id=assessment.id,
        title=assessment.title,
        competency_domain=assessment.competency_domain,
        competency_skill=assessment.competency_skill,
        difficulty=assessment.difficulty,
        questions=[
            QuestionOutForLearner(
                id=q.id,
                question=q.question,
                options=json.loads(q.options),
                competency=q.competency,
                difficulty=q.difficulty,
            )
            for q in assessment.questions
        ],
    )


@router.post(
    "/evaluate",
    response_model=EvaluateAssessmentResponse,
    summary="Submit assessment answers for grading",
    description=(
        "Grades the submission, deterministically updates the learner's competency estimate "
        "for the assessed skill (blending prior evidence with this attempt), recomputes skill "
        "gaps, and returns the next recommended quiz difficulty (adaptive learning)."
    ),
)
def evaluate_assessment(
    payload: EvaluateAssessmentRequest, db: Session = Depends(get_db)
) -> EvaluateAssessmentResponse:
    try:
        result = assessment_engine.evaluate_assessment(
            db,
            assessment_id=payload.assessment_id,
            employee_id=payload.employee_id,
            answers=payload.answers,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        logger.exception("Assessment evaluation failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to evaluate assessment."
        ) from exc

    return EvaluateAssessmentResponse(**result)
