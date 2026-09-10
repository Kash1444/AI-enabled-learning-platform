"""
Adaptive Learning.

Keeps the learning loop closing after every assessment attempt:

    score < ADAPTIVE_EASY_MAX_PCT%            -> next quiz: Easy
    ADAPTIVE_EASY_MAX_PCT-ADAPTIVE_INTERMEDIATE_MAX_PCT % -> next quiz: Intermediate
    > ADAPTIVE_INTERMEDIATE_MAX_PCT%          -> next quiz: Advanced

Thresholds are configurable (see app/core/config.py / `.env`). The actual
competency-score update and skill-gap recompute happen in
assessment_engine.evaluate_assessment(); this module only owns the
"what should happen next" decision, which keeps that concern testable in
isolation.
"""

from __future__ import annotations

from app.core.config import get_settings

settings = get_settings()


def next_difficulty_for_score(percentage: float) -> str:
    if percentage < settings.ADAPTIVE_EASY_MAX_PCT:
        return "Easy"
    if percentage < settings.ADAPTIVE_INTERMEDIATE_MAX_PCT:
        return "Intermediate"
    return "Advanced"


def reprioritize_note(skill: str, percentage: float) -> str:
    """Human-readable explanation of the adaptive effect of one attempt,
    used in assistant answers / feedback text."""
    if percentage < settings.ADAPTIVE_EASY_MAX_PCT:
        return (
            f"Because performance on {skill} was below {settings.ADAPTIVE_EASY_MAX_PCT:.0f}%, "
            f"{skill} becomes a higher-priority recommendation and future quizzes on it will "
            f"start at an easier difficulty."
        )
    if percentage < settings.ADAPTIVE_INTERMEDIATE_MAX_PCT:
        return (
            f"Performance on {skill} was moderate; intermediate-level material remains "
            f"recommended for continued improvement."
        )
    return (
        f"Performance on {skill} was strong; future quizzes on it will move to an advanced "
        f"difficulty and lower-priority recommendations may be surfaced instead."
    )
