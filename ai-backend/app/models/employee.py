"""Employee and Role database models."""

from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, utcnow


class Role(Base):
    """A job role, e.g. 'Statistical Officer'. Requirements live in
    RoleCompetencyRequirement (one row per competency domain)."""

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, default="")

    requirements: Mapped[List["RoleCompetencyRequirement"]] = relationship(
        back_populates="role", cascade="all, delete-orphan"
    )
    employees: Mapped[List["Employee"]] = relationship(back_populates="role")


class RoleCompetencyRequirement(Base):
    """Required competency level (1-5 scale) for a role, per domain."""

    __tablename__ = "role_competency_requirements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    domain: Mapped[str] = mapped_column(String(80), index=True)
    required_level: Mapped[float] = mapped_column(default=3.0)

    role: Mapped["Role"] = relationship(back_populates="requirements")


class Employee(Base):
    """A learner/employee profile."""

    __tablename__ = "employees"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)  # e.g. EMP001
    name: Mapped[str] = mapped_column(String(150))
    designation: Mapped[str] = mapped_column(String(150), default="")
    department: Mapped[str] = mapped_column(String(200), default="")
    organization: Mapped[str] = mapped_column(String(200), default="")
    email: Mapped[str] = mapped_column(String(200), default="")
    location: Mapped[str] = mapped_column(String(120), default="")
    experience_years: Mapped[int] = mapped_column(Integer, default=0)
    education: Mapped[str] = mapped_column(String(200), default="")
    joining_year: Mapped[int] = mapped_column(Integer, default=utcnow().year)

    role_id: Mapped[int | None] = mapped_column(ForeignKey("roles.id"), nullable=True)
    role: Mapped["Role"] = relationship(back_populates="employees")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
