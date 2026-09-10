"""
Skill Gap Engine.

    gap = required_level - current_level
    priority = High   if gap >= GAP_HIGH_THRESHOLD
               Medium if gap >= GAP_MEDIUM_THRESHOLD
               Low    otherwise

Thresholds are configurable via `.env` (GAP_HIGH_THRESHOLD /
GAP_MEDIUM_THRESHOLD, see app/core/config.py) rather than hardcoded, per
the SIH deliverable's explainability requirement. Every gap produced here
also carries a human-readable explanation of *why* it was flagged, so the
frontend (or the AI assistant) can always answer "why is this a gap?".
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.competency import SkillGapRecord
from app.models.employee import Employee
from app.services.competency_engine import get_role_requirement_map, latest_skill_levels

settings = get_settings()


@dataclass
class SkillGap:
    skill: str
    domain: str
    current: float
    required: float
    gap: float
    priority: str
    description: str
    recommended_action: str


def classify_priority(gap: float) -> str:
    if gap >= settings.GAP_HIGH_THRESHOLD:
        return "High"
    if gap >= settings.GAP_MEDIUM_THRESHOLD:
        return "Medium"
    return "Low"


def _describe_gap(skill: str, domain: str, current: float, required: float, role_name: str) -> str:
    if current <= 0:
        return (
            f"No assessment data yet for {skill}; the {domain} domain requires a level of "
            f"{required:.1f}/5 for the {role_name} role."
        )
    return (
        f"The learner demonstrated a competency level of {current:.1f}/5 in {skill}, which is "
        f"below the {required:.1f}/5 required for the {role_name} role."
    )


def _recommend_action(skill: str, priority: str) -> str:
    if priority == "High":
        return f"Prioritize a focused learning module and take a follow-up assessment on {skill} soon."
    if priority == "Medium":
        return f"Schedule a learning module on {skill} in your current learning path."
    return f"Consider a refresher module on {skill} when convenient."


def compute_skill_gaps(db: Session, employee: Employee, *, only_gaps: bool = True) -> List[SkillGap]:
    """
    Compute a SkillGap for every skill the employee has been assessed on,
    comparing it against the domain-level requirement for their role.

    `only_gaps=True` (default) drops skills with a non-positive gap (i.e.
    the learner already meets or exceeds the requirement).
    """
    skill_levels = latest_skill_levels(db, employee.id)
    role_name = employee.role.name if employee.role else "your role"
    requirements = get_role_requirement_map(db, employee.role.name if employee.role else None)

    gaps: List[SkillGap] = []
    for skill, data in skill_levels.items():
        domain = data["domain"]
        current = data["level"]
        required = requirements.get(domain, 3.5)
        gap = round(required - current, 2)
        if only_gaps and gap <= 0:
            continue
        gap = max(gap, 0.0)
        priority = classify_priority(gap)
        gaps.append(
            SkillGap(
                skill=skill,
                domain=domain,
                current=current,
                required=required,
                gap=gap,
                priority=priority,
                description=_describe_gap(skill, domain, current, required, role_name),
                recommended_action=_recommend_action(skill, priority),
            )
        )
    gaps.sort(key=lambda g: g.gap, reverse=True)
    return gaps


def persist_skill_gaps(db: Session, employee_id: str, gaps: List[SkillGap]) -> None:
    """Replace the stored skill-gap snapshot for an employee with the latest
    computation, so other endpoints can read it without recomputing."""
    db.query(SkillGapRecord).filter(SkillGapRecord.employee_id == employee_id).delete()
    for g in gaps:
        db.add(
            SkillGapRecord(
                employee_id=employee_id,
                skill=g.skill,
                domain=g.domain,
                current=g.current,
                required=g.required,
                gap=g.gap,
                priority=g.priority,
                description=g.description,
                recommended_action=g.recommended_action,
            )
        )
    db.commit()


def summarize_gaps(gaps: List[SkillGap]) -> Dict[str, float | int]:
    return {
        "total_gaps": len(gaps),
        "high_priority_gaps": sum(1 for g in gaps if g.priority == "High"),
        "medium_priority_gaps": sum(1 for g in gaps if g.priority == "Medium"),
        "low_priority_gaps": sum(1 for g in gaps if g.priority == "Low"),
        "total_competency_gap": round(sum(g.gap for g in gaps), 2),
    }
