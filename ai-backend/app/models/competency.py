"""Competency catalog, scores and skill-gap models."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, utcnow


class Competency(Base):
    """
    A single skill/competency in the extensible catalog, e.g. ("Technical",
    "Python"). The catalog itself is defined in app/data/competencies.py and
    synced into this table on startup/seed - the *architecture* is not
    hardcoded to any fixed skill list.
    """

    __tablename__ = "competencies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    domain: Mapped[str] = mapped_column(String(80), index=True)
    skill: Mapped[str] = mapped_column(String(150), index=True)
    description: Mapped[str] = mapped_column(Text, default="")

    __table_args__ = ()


class CompetencyScore(Base):
    """
    An employee's current level (1-5) for a given skill, produced by the
    deterministic competency engine. History is preserved by inserting a
    new row on every update (see services/competency_engine.py) so we keep
    an auditable timeline without extra tables.
    """

    __tablename__ = "competency_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    employee_id: Mapped[str] = mapped_column(ForeignKey("employees.id"), index=True)
    domain: Mapped[str] = mapped_column(String(80), index=True)
    skill: Mapped[str] = mapped_column(String(150), index=True)
    level: Mapped[float] = mapped_column(Float)  # 1.0 - 5.0
    source: Mapped[str] = mapped_column(String(40), default="assessment")  # assessment|seed|adaptive
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, index=True)


class SkillGapRecord(Base):
    """
    A persisted snapshot of an identified skill gap. Recomputed whenever
    competency scores change (see services/skill_gap_engine.py) so the
    frontend can read the latest gaps without recalculating client-side.
    """

    __tablename__ = "skill_gaps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    employee_id: Mapped[str] = mapped_column(ForeignKey("employees.id"), index=True)
    skill: Mapped[str] = mapped_column(String(150))
    domain: Mapped[str] = mapped_column(String(80))
    current: Mapped[float] = mapped_column(Float)
    required: Mapped[float] = mapped_column(Float)
    gap: Mapped[float] = mapped_column(Float)
    priority: Mapped[str] = mapped_column(String(20))  # High|Medium|Low
    description: Mapped[str] = mapped_column(Text, default="")
    recommended_action: Mapped[str] = mapped_column(Text, default="")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
