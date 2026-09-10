"""Pydantic schemas for the recommendation engine and iGOT/NSSTA providers."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class RecommendationItem(BaseModel):
    """Matches (and extends) the existing `aiRecommendations` mock shape in
    frontend/src/data/employeeData.js: id, title, provider, category, level,
    duration, reason, progress, action - plus explainability fields used by
    the recommendation engine (skill, relevanceScore, priority, sourceUrl)."""

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
    relevanceScore: float
    type: str  # Course | Program | Module
    sourceUrl: Optional[str] = None
    isDemoData: bool = True


class RecommendationListResponse(BaseModel):
    employee_id: str
    recommendations: List[RecommendationItem]


class CourseItem(BaseModel):
    """Matches the shape used by IGOTCourses.jsx."""

    id: str
    title: str
    category: str
    level: str
    duration: str
    progress: int
    status: str
    description: str
    skill: str
    priority: str
    icon: str
    provider: str
    url: Optional[str] = None
    isDemoData: bool = True


class CourseListResponse(BaseModel):
    employee_id: str
    source: str  # "mock" | "live"
    courses: List[CourseItem]


class ProgramItem(BaseModel):
    """Matches the shape used by NSSTAPrograms.jsx."""

    id: str
    title: str
    category: str
    provider: str
    duration: str
    level: str
    mode: str
    skill: str
    currentLevel: float
    requiredLevel: float
    priority: str
    recommended: bool
    description: str
    reason: str
    isDemoData: bool = True


class ProgramListResponse(BaseModel):
    employee_id: str
    source: str
    programs: List[ProgramItem]
