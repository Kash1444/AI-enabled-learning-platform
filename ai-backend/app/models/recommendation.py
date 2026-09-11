"""Learning resources, recommendations and learner progress models."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, utcnow


class LearningResource(Base):
    """
    A catalog entry for a learning resource. Populated from either the
    mock iGOT/NSSTA providers (see app/integrations) or generic internal
    resources (app/data/demo_data.py). The recommendation engine ranks
    rows from this table.
    """

    __tablename__ = "learning_resources"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)  # res_<uuid>
    title: Mapped[str] = mapped_column(String(250))
    provider: Mapped[str] = mapped_column(String(120))  # "iGOT Karmayogi" | "NSSTA TPAC" | "NSSTA" | "Internal"
    provider_type: Mapped[str] = mapped_column(String(20))  # igot|nssta|internal
    resource_type: Mapped[str] = mapped_column(String(40), default="Course")  # Course|Program|Module
    category: Mapped[str] = mapped_column(String(80), default="")  # competency domain
    skill: Mapped[str] = mapped_column(String(150), default="")
    level: Mapped[str] = mapped_column(String(20), default="Intermediate")
    duration_hours: Mapped[float] = mapped_column(Float, default=4.0)
    description: Mapped[str] = mapped_column(Text, default="")
    url: Mapped[str] = mapped_column(String(400), default="")
    is_demo_data: Mapped[bool] = mapped_column(default=True)


class Recommendation(Base):
    """A ranked recommendation of a LearningResource for a given employee."""

    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    employee_id: Mapped[str] = mapped_column(ForeignKey("employees.id"), index=True)
    resource_id: Mapped[str] = mapped_column(ForeignKey("learning_resources.id"))
    skill: Mapped[str] = mapped_column(String(150))
    domain: Mapped[str] = mapped_column(String(80))
    relevance_score: Mapped[float] = mapped_column(Float)
    priority: Mapped[str] = mapped_column(String(20))
    reason: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class LearningProgress(Base):
    """Tracks an employee's progress against a learning resource."""

    __tablename__ = "learning_progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    employee_id: Mapped[str] = mapped_column(ForeignKey("employees.id"), index=True)
    resource_id: Mapped[str] = mapped_column(ForeignKey("learning_resources.id"))
    progress_pct: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), default="Not Started")  # Not Started|In Progress|Completed
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
