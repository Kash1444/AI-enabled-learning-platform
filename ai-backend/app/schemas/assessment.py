"""Pydantic schemas for assessment generation, retrieval and evaluation."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator

Difficulty = Literal["Easy", "Intermediate", "Advanced"]


class GenerateAssessmentRequest(BaseModel):
    material_id: Optional[str] = Field(
        None, description="If provided, questions are grounded in this uploaded material via RAG."
    )
    competency: str = Field(..., examples=["Sampling Methodology"])
    domain: str = Field("Statistical", examples=["Statistical"])
    num_questions: int = Field(5, ge=1, le=20)
    difficulty: Difficulty = "Intermediate"
    employee_id: Optional[str] = Field(None, description="Personalizes title/labelling only")


class QuestionOut(BaseModel):
    id: str
    question: str
    options: List[str]
    correct_answer: int
    explanation: str
    competency: str
    difficulty: str
    source: str


class QuestionOutForLearner(BaseModel):
    """Same as QuestionOut but WITHOUT the answer key - what a learner taking
    the quiz should receive from GET /api/assessment/{id}."""

    id: str
    question: str
    options: List[str]
    competency: str
    difficulty: str


class AssessmentResponse(BaseModel):
    id: str
    title: str
    competency_domain: str
    competency_skill: str
    difficulty: str
    material_id: Optional[str] = None
    generated_by: str
    created_at: datetime
    questions: List[QuestionOut]


class AssessmentResponseForLearner(BaseModel):
    id: str
    title: str
    competency_domain: str
    competency_skill: str
    difficulty: str
    questions: List[QuestionOutForLearner]


class EvaluateAssessmentRequest(BaseModel):
    assessment_id: str
    employee_id: str
    answers: Dict[str, int] = Field(
        ..., description="Mapping of question_id -> chosen option index", examples=[{"q_123": 1}]
    )

    @field_validator("answers")
    @classmethod
    def _non_empty(cls, v: Dict[str, int]) -> Dict[str, int]:
        if not v:
            raise ValueError("answers must not be empty")
        return v


class PerQuestionResult(BaseModel):
    question_id: str
    question: str
    correct: bool
    chosen_index: Optional[int]
    correct_index: int
    explanation: str
    competency: str


class CompetencyImpact(BaseModel):
    skill: str
    domain: str
    before: float
    after: float
    delta: float


class EvaluateAssessmentResponse(BaseModel):
    attempt_id: str
    assessment_id: str
    employee_id: str
    score: int
    total: int
    percentage: float
    correct_count: int
    incorrect_count: int
    results: List[PerQuestionResult]
    competency_impact: List[CompetencyImpact]
    feedback: str
    next_recommended_difficulty: Difficulty
    new_skill_gaps: List[str] = Field(
        default_factory=list, description="Skills newly flagged as gaps after this attempt"
    )
