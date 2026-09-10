"""Competency & skill-gap endpoints."""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.employee import Employee
from app.schemas.competency import (
    CompetencyAssessRequest,
    CompetencyAssessResult,
    CompetencyOverviewResponse,
    SkillGapItem,
    SkillGapSummary,
)
from app.services import competency_engine, skill_gap_engine
from app.services.competency_engine import get_domain_scores

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/competency", tags=["Competency"])


def _get_employee_or_404(db: Session, employee_id: str) -> Employee:
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee '{employee_id}' not found.")
    return employee


@router.post(
    "/assess",
    response_model=CompetencyAssessResult,
    summary="Submit assessment answers and get deterministic competency scores",
    description=(
        "Scores a set of answers using a transparent, reproducible formula "
        "(correctness + difficulty + question weight -> 1-5 level per skill), "
        "persists the new scores, and returns the updated domain-level view. "
        "This never asks an LLM to guess a number."
    ),
)
def assess_competency(payload: CompetencyAssessRequest, db: Session = Depends(get_db)) -> CompetencyAssessResult:
    employee = _get_employee_or_404(db, payload.employee_id)

    scored = competency_engine.score_assessment(payload.answers)
    if not scored:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No valid answers supplied.")

    competency_engine.persist_scores(db, employee.id, scored, source="assessment")
    db.refresh(employee)

    domain_scores = get_domain_scores(db, employee)
    gaps = skill_gap_engine.compute_skill_gaps(db, employee)
    skill_gap_engine.persist_skill_gaps(db, employee.id, gaps)

    return CompetencyAssessResult(
        employee_id=employee.id,
        domain_scores=domain_scores,
        skill_levels={skill: data["level"] for skill, data in scored.items()},
        explanation=[f"{skill}: {data['explanation']}" for skill, data in scored.items()],
        feedback=(
            f"Recorded scores for {len(scored)} skill(s). "
            f"{sum(1 for g in gaps if g.priority == 'High')} high-priority gap(s) remain."
        ),
    )


@router.get(
    "/{employee_id}",
    response_model=CompetencyOverviewResponse,
    summary="Get an employee's competency overview",
    description="Returns overall competency %, current/required totals and per-domain scores, "
    "matching the shape used by the 'My Competencies' page.",
)
def get_competency_overview(employee_id: str, db: Session = Depends(get_db)) -> CompetencyOverviewResponse:
    employee = _get_employee_or_404(db, employee_id)
    domains = get_domain_scores(db, employee)

    total_current = round(sum(d.current for d in domains), 2)
    total_required = round(sum(d.required for d in domains), 2)
    overall_pct = int(round((total_current / total_required) * 100)) if total_required else 0

    return CompetencyOverviewResponse(
        employee_id=employee.id,
        overall_competency_pct=overall_pct,
        current_score=total_current,
        required_score=total_required,
        total_gap=round(total_required - total_current, 2),
        domains=domains,
    )


@router.get(
    "/{employee_id}/gaps",
    response_model=SkillGapSummary,
    summary="Get an employee's skill gap analysis",
    description="Computes gap = required - current per skill, classifies priority using "
    "configurable thresholds, and returns a full explainable breakdown.",
)
def get_skill_gaps(employee_id: str, db: Session = Depends(get_db)) -> SkillGapSummary:
    employee = _get_employee_or_404(db, employee_id)
    gaps = skill_gap_engine.compute_skill_gaps(db, employee)
    skill_gap_engine.persist_skill_gaps(db, employee.id, gaps)
    summary = skill_gap_engine.summarize_gaps(gaps)

    items = [
        SkillGapItem(
            id=i + 1,
            skill=g.skill,
            domain=g.domain,
            current=g.current,
            required=g.required,
            gap=g.gap,
            priority=g.priority,
            description=g.description,
            recommendedAction=g.recommended_action,
        )
        for i, g in enumerate(gaps)
    ]

    return SkillGapSummary(
        employee_id=employee.id,
        total_gaps=summary["total_gaps"],
        high_priority_gaps=summary["high_priority_gaps"],
        medium_priority_gaps=summary["medium_priority_gaps"],
        low_priority_gaps=summary["low_priority_gaps"],
        total_competency_gap=summary["total_competency_gap"],
        gaps=items,
    )
