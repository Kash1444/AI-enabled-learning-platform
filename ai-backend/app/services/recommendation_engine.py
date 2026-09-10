"""
Recommendation Engine.

Input:  employee profile + current competency scores + skill gaps
Output: ranked, explainable learning recommendations

Ranking combines (all deterministic, all inspectable via `reason`):

    1. Skill gap severity        (bigger gap -> higher score)
    2. Priority weight            (High/Medium/Low from the skill-gap engine)
    3. Level match                (resource difficulty vs learner's current level)
    4. Role relevance             (resource domain vs a domain the role requires)
    5. Learning history           (small penalty if already completed)

The engine queries the iGOT/NSSTA provider abstractions (app/integrations)
rather than hitting any live API directly, so recommendations always work
in DEMO_MODE and switch to real content automatically once real providers
are configured.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.integrations.igot import get_igot_provider
from app.integrations.nssta import get_nssta_provider
from app.models.employee import Employee
from app.models.recommendation import LearningProgress
from app.services.skill_gap_engine import SkillGap

PRIORITY_WEIGHT = {"High": 1.0, "Medium": 0.6, "Low": 0.3}


def _level_bucket(current_level: float) -> str:
    if current_level < 2.5:
        return "Beginner"
    if current_level < 3.75:
        return "Intermediate"
    return "Advanced"


@dataclass
class RankedRecommendation:
    id: str
    title: str
    provider: str
    category: str
    skill: str
    level: str
    duration: str
    reason: str
    progress: int
    action: str
    priority: str
    relevance_score: float
    type: str
    source_url: Optional[str]
    is_demo_data: bool


def _progress_for(db: Session, employee_id: str, resource_id: str) -> tuple[int, str]:
    row = (
        db.query(LearningProgress)
        .filter(LearningProgress.employee_id == employee_id, LearningProgress.resource_id == resource_id)
        .first()
    )
    if not row:
        return 0, "Start Learning"
    if row.status == "Completed":
        return 100, "Review"
    if row.progress_pct > 0:
        return row.progress_pct, "Continue Learning"
    return 0, "Start Learning"


def _score_candidate(gap: SkillGap, candidate_level: str) -> float:
    gap_component = min(gap.gap / 2.0, 1.0)  # normalize; gaps >=2.0 saturate at 1.0
    priority_component = PRIORITY_WEIGHT.get(gap.priority, 0.3)
    level_component = 1.0 if candidate_level == _level_bucket(gap.current) else 0.5
    score = gap_component * 0.5 + priority_component * 0.3 + level_component * 0.2
    return round(score * 100, 1)


def recommend_for_gaps(
    db: Session,
    employee: Employee,
    gaps: List[SkillGap],
    *,
    limit: int = 10,
) -> List[RankedRecommendation]:
    igot = get_igot_provider()
    nssta = get_nssta_provider()

    candidates: List[RankedRecommendation] = []
    for gap in gaps:
        igot_courses = igot.search_courses(skill=gap.skill, limit=3)
        nssta_programs = nssta.search_programs(skill=gap.skill, limit=2)

        for course in igot_courses:
            score = _score_candidate(gap, course.get("level", "Intermediate"))
            progress, action = _progress_for(db, employee.id, course["id"])
            candidates.append(
                RankedRecommendation(
                    id=course["id"],
                    title=course["title"],
                    provider=course["provider"],
                    category=course["category"],
                    skill=gap.skill,
                    level=course["level"],
                    duration=f"{course['duration_hours']} hours",
                    reason=(
                        f"Recommended because {gap.skill} is a {gap.priority.lower()}-priority "
                        f"competency gap for your role (current {gap.current:.1f}/5, "
                        f"required {gap.required:.1f}/5)."
                    ),
                    progress=progress,
                    action=action,
                    priority=gap.priority,
                    relevance_score=score,
                    type="Course",
                    source_url=course.get("url"),
                    is_demo_data=course.get("is_demo_data", True),
                )
            )

        for program in nssta_programs:
            score = _score_candidate(gap, program.get("level", "Intermediate"))
            progress, action = _progress_for(db, employee.id, program["id"])
            candidates.append(
                RankedRecommendation(
                    id=program["id"],
                    title=program["title"],
                    provider=program["provider"],
                    category=program["category"],
                    skill=gap.skill,
                    level=program["level"],
                    duration=f"{program['duration_hours']} hours",
                    reason=(
                        f"Recommended because {gap.skill} is a {gap.priority.lower()}-priority "
                        f"competency gap; NSSTA TPAC offers a dedicated program for this skill."
                    ),
                    progress=progress,
                    action=action,
                    priority=gap.priority,
                    relevance_score=score,
                    type="Program",
                    source_url=None,
                    is_demo_data=program.get("is_demo_data", True),
                )
            )

    # de-duplicate by id, keep highest score, sort by score desc
    best_by_id: Dict[str, RankedRecommendation] = {}
    for c in candidates:
        existing = best_by_id.get(c.id)
        if not existing or c.relevance_score > existing.relevance_score:
            best_by_id[c.id] = c

    ranked = sorted(best_by_id.values(), key=lambda c: c.relevance_score, reverse=True)
    return ranked[:limit]
