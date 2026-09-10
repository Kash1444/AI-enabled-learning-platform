"""Recommendation, iGOT course and NSSTA program endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.integrations.igot import get_igot_provider
from app.integrations.nssta import get_nssta_provider
from app.models.employee import Employee
from app.schemas.recommendation import (
    CourseItem,
    CourseListResponse,
    ProgramItem,
    ProgramListResponse,
    RecommendationItem,
    RecommendationListResponse,
)
from app.services.recommendation_engine import recommend_for_gaps
from app.services.skill_gap_engine import compute_skill_gaps

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])


def _get_employee_or_404(db: Session, employee_id: str) -> Employee:
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee '{employee_id}' not found.")
    return employee


@router.get(
    "/{employee_id}",
    response_model=RecommendationListResponse,
    summary="Get personalized learning recommendations",
    description=(
        "Ranks iGOT/NSSTA/internal resources against the employee's current skill gaps using "
        "gap severity, priority, level match and role relevance. Matches the "
        "`aiRecommendations` shape already used by the frontend mock data."
    ),
)
def get_recommendations(
    employee_id: str, limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)
) -> RecommendationListResponse:
    employee = _get_employee_or_404(db, employee_id)
    gaps = compute_skill_gaps(db, employee)
    ranked = recommend_for_gaps(db, employee, gaps, limit=limit)

    items = [
        RecommendationItem(
            id=r.id,
            title=r.title,
            provider=r.provider,
            category=r.category,
            skill=r.skill,
            level=r.level,
            duration=r.duration,
            reason=r.reason,
            progress=r.progress,
            action=r.action,
            priority=r.priority,
            relevanceScore=r.relevance_score,
            type=r.type,
            sourceUrl=r.source_url,
            isDemoData=r.is_demo_data,
        )
        for r in ranked
    ]
    return RecommendationListResponse(employee_id=employee.id, recommendations=items)


@router.get(
    "/{employee_id}/igot",
    response_model=CourseListResponse,
    summary="Get recommended iGOT Karmayogi courses",
    description=(
        "Returns iGOT-style courses relevant to the employee's skill gaps via the "
        "IGOTProvider abstraction. Uses demo/mock data unless IGOT_API_BASE_URL and "
        "IGOT_API_KEY are configured, in which case `source` becomes 'live'."
    ),
)
def get_igot_courses(employee_id: str, db: Session = Depends(get_db)) -> CourseListResponse:
    employee = _get_employee_or_404(db, employee_id)
    gaps = compute_skill_gaps(db, employee)
    provider = get_igot_provider()
    is_mock = provider.__class__.__name__ == "MockIGOTProvider"

    gap_skills = {g.skill: g for g in gaps}
    courses: list[CourseItem] = []
    seen_ids: set[str] = set()

    for gap in gaps:
        for course in provider.search_courses(skill=gap.skill, limit=3):
            if course["id"] in seen_ids:
                continue
            seen_ids.add(course["id"])
            courses.append(
                CourseItem(
                    id=course["id"],
                    title=course["title"],
                    category=course["category"],
                    level=course["level"],
                    duration=f"{course['duration_hours']} hours",
                    progress=0,
                    status="Not Started",
                    description=course["description"],
                    skill=course["skill"],
                    priority=gap.priority,
                    icon=course.get("icon", "📘"),
                    provider=course["provider"],
                    url=course.get("url"),
                    isDemoData=course.get("is_demo_data", True),
                )
            )

    # If the learner has no gaps yet, still show a general catalog so the page isn't empty.
    if not courses:
        for course in provider.search_courses(limit=8):
            courses.append(
                CourseItem(
                    id=course["id"],
                    title=course["title"],
                    category=course["category"],
                    level=course["level"],
                    duration=f"{course['duration_hours']} hours",
                    progress=0,
                    status="Not Started",
                    description=course["description"],
                    skill=course["skill"],
                    priority="Low",
                    icon=course.get("icon", "📘"),
                    provider=course["provider"],
                    url=course.get("url"),
                    isDemoData=course.get("is_demo_data", True),
                )
            )

    return CourseListResponse(employee_id=employee.id, source="mock" if is_mock else "live", courses=courses)


@router.get(
    "/{employee_id}/nssta",
    response_model=ProgramListResponse,
    summary="Get recommended NSSTA TPAC training programs",
    description=(
        "Returns NSSTA-style training programs relevant to the employee's skill gaps via the "
        "NSSTAProvider abstraction. Uses demo/mock data unless NSSTA_API_BASE_URL and "
        "NSSTA_API_KEY are configured."
    ),
)
def get_nssta_programs(employee_id: str, db: Session = Depends(get_db)) -> ProgramListResponse:
    employee = _get_employee_or_404(db, employee_id)
    gaps = compute_skill_gaps(db, employee)
    provider = get_nssta_provider()
    is_mock = provider.__class__.__name__ == "MockNSSTAProvider"

    programs: list[ProgramItem] = []
    seen_ids: set[str] = set()

    for gap in gaps:
        for program in provider.search_programs(skill=gap.skill, limit=2):
            if program["id"] in seen_ids:
                continue
            seen_ids.add(program["id"])
            programs.append(
                ProgramItem(
                    id=program["id"],
                    title=program["title"],
                    category=program["category"],
                    provider=program["provider"],
                    duration=f"{program['duration_hours']} hours",
                    level=program["level"],
                    mode=program["mode"],
                    skill=program["skill"],
                    currentLevel=gap.current,
                    requiredLevel=gap.required,
                    priority=gap.priority,
                    recommended=True,
                    description=program.get("reason", ""),
                    reason=program.get("reason", ""),
                    isDemoData=program.get("is_demo_data", True),
                )
            )

    if not programs:
        for program in provider.search_programs(limit=6):
            programs.append(
                ProgramItem(
                    id=program["id"],
                    title=program["title"],
                    category=program["category"],
                    provider=program["provider"],
                    duration=f"{program['duration_hours']} hours",
                    level=program["level"],
                    mode=program["mode"],
                    skill=program["skill"],
                    currentLevel=0.0,
                    requiredLevel=0.0,
                    priority="Low",
                    recommended=False,
                    description=program.get("reason", ""),
                    reason=program.get("reason", ""),
                    isDemoData=program.get("is_demo_data", True),
                )
            )

    return ProgramListResponse(employee_id=employee.id, source="mock" if is_mock else "live", programs=programs)
