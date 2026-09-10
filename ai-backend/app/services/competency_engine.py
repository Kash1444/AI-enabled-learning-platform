"""
Competency Assessment Engine.

This is the "do not fake AI" core of the platform: competency levels are
NEVER produced by asking an LLM to guess a number. They come from a
transparent, reproducible formula over the learner's actual assessment
answers:

    weighted_correctness = sum(correct_i * weight_i * difficulty_multiplier_i)
                            -------------------------------------------------
                            sum(weight_i * difficulty_multiplier_i)

    skill_level (1-5)     = 1 + 4 * weighted_correctness

An (optional) LLM may add a qualitative feedback *sentence* on top of this
number, but the number itself is always deterministic and auditable - the
same answers always produce the same score, and `explain_skill_score()`
can show exactly why.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from datetime import datetime
from typing import Dict, List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.data.competencies import domain_for_skill
from app.data.roles import get_role_requirements
from app.models.competency import CompetencyScore
from app.models.employee import Employee, RoleCompetencyRequirement
from app.schemas.competency import AnswerInput, DomainScore

logger = logging.getLogger(__name__)

DIFFICULTY_MULTIPLIER = {"Easy": 1.0, "Intermediate": 1.3, "Advanced": 1.6}
DEFAULT_REQUIRED_LEVEL = 3.5


def score_answers_for_skill(answers: List[AnswerInput]) -> tuple[float, str]:
    """Deterministically score one skill's worth of answers -> (level, explanation)."""
    numerator = 0.0
    denominator = 0.0
    correct_count = 0
    for a in answers:
        multiplier = DIFFICULTY_MULTIPLIER.get(a.difficulty, 1.0)
        w = a.weight * multiplier
        denominator += w
        if a.is_correct:
            numerator += w
            correct_count += 1
    if denominator == 0:
        fraction = 0.0
    else:
        fraction = numerator / denominator
    level = round(1 + 4 * fraction, 2)
    level = max(1.0, min(5.0, level))
    explanation = (
        f"{correct_count}/{len(answers)} correct, difficulty-and-weight-adjusted score "
        f"{fraction:.2f} -> level {level:.1f}/5."
    )
    return level, explanation


def score_assessment(answers: List[AnswerInput]) -> Dict[str, dict]:
    """
    Group answers by skill and score each skill independently.

    Returns: {skill: {"level": float, "domain": str, "explanation": str}}
    """
    by_skill: Dict[str, List[AnswerInput]] = defaultdict(list)
    for a in answers:
        by_skill[a.skill].append(a)

    results: Dict[str, dict] = {}
    for skill, skill_answers in by_skill.items():
        level, explanation = score_answers_for_skill(skill_answers)
        domain = skill_answers[0].domain or domain_for_skill(skill)
        results[skill] = {"level": level, "domain": domain, "explanation": explanation}
    return results


def persist_scores(db: Session, employee_id: str, scored: Dict[str, dict], source: str = "assessment") -> None:
    """Insert a new CompetencyScore row per skill (append-only history)."""
    now = datetime.utcnow()
    for skill, data in scored.items():
        db.add(
            CompetencyScore(
                employee_id=employee_id,
                domain=data["domain"],
                skill=skill,
                level=data["level"],
                source=source,
                created_at=now,
            )
        )
    db.commit()


def latest_skill_levels(db: Session, employee_id: str) -> Dict[str, dict]:
    """
    Return the most recent level per skill for an employee:
    {skill: {"level": float, "domain": str}}
    """
    subq = (
        db.query(
            CompetencyScore.skill,
            func.max(CompetencyScore.created_at).label("max_created"),
        )
        .filter(CompetencyScore.employee_id == employee_id)
        .group_by(CompetencyScore.skill)
        .subquery()
    )
    rows = (
        db.query(CompetencyScore)
        .join(
            subq,
            (CompetencyScore.skill == subq.c.skill) & (CompetencyScore.created_at == subq.c.max_created),
        )
        .filter(CompetencyScore.employee_id == employee_id)
        .all()
    )
    return {r.skill: {"level": r.level, "domain": r.domain} for r in rows}


def get_role_requirement_map(db: Session, role_name: str | None) -> Dict[str, float]:
    """Look up domain requirements from the DB (seeded RoleCompetencyRequirement
    rows) with a fallback to the in-code default matrix (app/data/roles.py)."""
    if role_name:
        req_rows = (
            db.query(RoleCompetencyRequirement)
            .join(RoleCompetencyRequirement.role)
            .filter(RoleCompetencyRequirement.role.has(name=role_name))
            .all()
        )
        if req_rows:
            return {r.domain: r.required_level for r in req_rows}
    return get_role_requirements(role_name or "")


def get_domain_scores(db: Session, employee: Employee) -> List[DomainScore]:
    """Aggregate the latest per-skill levels into per-domain current scores,
    compared against the employee's role requirements."""
    skill_levels = latest_skill_levels(db, employee.id)
    role_name = employee.role.name if employee.role else None
    requirements = get_role_requirement_map(db, role_name)

    by_domain: Dict[str, List[float]] = defaultdict(list)
    for data in skill_levels.values():
        by_domain[data["domain"]].append(data["level"])

    domains = set(by_domain.keys()) | set(requirements.keys())
    result: List[DomainScore] = []
    for domain in sorted(domains):
        current = round(sum(by_domain[domain]) / len(by_domain[domain]), 2) if by_domain.get(domain) else 0.0
        required = requirements.get(domain, DEFAULT_REQUIRED_LEVEL)
        result.append(DomainScore(domain=domain, current=current, required=required))
    return result
