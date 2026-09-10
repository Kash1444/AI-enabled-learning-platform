"""Pydantic request/response models for competency & skill-gap endpoints.

Field names intentionally mirror the shapes already consumed by the
existing React pages (Competencies.jsx, SkillGaps.jsx) so the frontend
service layer can pass API responses straight through with minimal glue.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class AnswerInput(BaseModel):
    question_id: str = Field(..., description="Identifier of the question being answered")
    skill: str = Field(..., description="Skill this question measures, e.g. 'Python'")
    domain: str = Field(..., description="Competency domain, e.g. 'Technical'")
    difficulty: str = Field("Intermediate", description="Easy | Intermediate | Advanced")
    is_correct: bool = Field(..., description="Whether the learner answered this question correctly")
    weight: float = Field(1.0, ge=0.1, le=5.0, description="Relative importance of this question")


class CompetencyAssessRequest(BaseModel):
    employee_id: str = Field(..., examples=["EMP001"])
    role: Optional[str] = Field(None, description="Overrides the employee's stored role, if provided")
    competency_domain: Optional[str] = Field(
        None, description="If set, only this domain's score is recalculated"
    )
    answers: List[AnswerInput] = Field(..., min_length=1)


class DomainScore(BaseModel):
    domain: str
    current: float
    required: float


class CompetencyAssessResult(BaseModel):
    employee_id: str
    domain_scores: List[DomainScore]
    skill_levels: dict[str, float] = Field(
        default_factory=dict, description="skill name -> new deterministic level (1-5)"
    )
    explanation: List[str] = Field(
        default_factory=list, description="Human-readable, per-skill scoring rationale"
    )
    feedback: str = Field("", description="Optional qualitative feedback (LLM if configured, else templated)")


class CompetencyOverviewResponse(BaseModel):
    employee_id: str
    overall_competency_pct: int
    current_score: float
    required_score: float
    total_gap: float
    domains: List[DomainScore]


class SkillGapItem(BaseModel):
    """Field names match the existing frontend `skillGaps` mock shape exactly
    (see frontend/src/data/employeeData.js) so this can be dropped straight
    into SkillGaps.jsx / Competencies.jsx without any remapping."""

    id: int
    skill: str
    domain: str
    current: float
    required: float
    gap: float
    priority: str
    description: str
    recommendedAction: str


class SkillGapSummary(BaseModel):
    employee_id: str
    total_gaps: int
    high_priority_gaps: int
    medium_priority_gaps: int
    low_priority_gaps: int
    total_competency_gap: float
    gaps: List[SkillGapItem]
