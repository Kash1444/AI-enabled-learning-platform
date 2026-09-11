"""Assessment (quiz), Question and AssessmentAttempt models."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, utcnow


class Assessment(Base):
    """A generated (or manually authored) set of MCQs."""

    __tablename__ = "assessments"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)  # asmt_<uuid>
    title: Mapped[str] = mapped_column(String(250))
    competency_domain: Mapped[str] = mapped_column(String(80), default="")
    competency_skill: Mapped[str] = mapped_column(String(150), default="")
    difficulty: Mapped[str] = mapped_column(String(20), default="Intermediate")
    material_id: Mapped[str | None] = mapped_column(String(40), nullable=True)
    generated_by: Mapped[str] = mapped_column(String(20), default="demo")  # demo|llm
    created_for_employee: Mapped[str | None] = mapped_column(String(40), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    questions: Mapped[list["Question"]] = relationship(
        back_populates="assessment", cascade="all, delete-orphan", order_by="Question.order_index"
    )


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)  # q_<uuid>
    assessment_id: Mapped[str] = mapped_column(ForeignKey("assessments.id"), index=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    question: Mapped[str] = mapped_column(Text)
    options: Mapped[str] = mapped_column(Text)  # JSON-encoded list[str]
    correct_answer: Mapped[int] = mapped_column(Integer)  # index into options
    explanation: Mapped[str] = mapped_column(Text, default="")
    competency: Mapped[str] = mapped_column(String(150), default="")
    difficulty: Mapped[str] = mapped_column(String(20), default="Intermediate")
    source: Mapped[str] = mapped_column(String(300), default="")
    source_chunk_id: Mapped[str | None] = mapped_column(String(60), nullable=True)
    weight: Mapped[float] = mapped_column(Float, default=1.0)

    assessment: Mapped["Assessment"] = relationship(back_populates="questions")


class AssessmentAttempt(Base):
    """A learner's submitted answers + computed results for one assessment."""

    __tablename__ = "assessment_attempts"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)  # attempt_<uuid>
    assessment_id: Mapped[str] = mapped_column(ForeignKey("assessments.id"), index=True)
    employee_id: Mapped[str] = mapped_column(ForeignKey("employees.id"), index=True)
    answers_json: Mapped[str] = mapped_column(Text)  # JSON-encoded {question_id: option_index}
    score: Mapped[int] = mapped_column(Integer)
    total: Mapped[int] = mapped_column(Integer)
    percentage: Mapped[float] = mapped_column(Float)
    competency_before: Mapped[float] = mapped_column(Float, default=0.0)
    competency_after: Mapped[float] = mapped_column(Float, default=0.0)
    feedback: Mapped[str] = mapped_column(Text, default="")
    next_difficulty: Mapped[str] = mapped_column(String(20), default="Intermediate")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
