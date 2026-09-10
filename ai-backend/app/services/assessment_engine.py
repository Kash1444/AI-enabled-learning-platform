"""
Assessment Engine.

Two responsibilities:

1. `generate_assessment()` — build a persisted Assessment + Questions,
   either:
     - grounded in an uploaded LearningMaterial via the RAG pipeline +
       MCQ generator (trainer flow, `POST /api/assessment/generate` with
       `material_id`), or
     - a generic, catalog-derived competency self-check when no material
       is supplied (employee "Start Assessment" flow).

2. `evaluate_assessment()` — score a learner's submitted answers,
   deterministically update their competency profile via the competency
   engine, recompute skill gaps, and hand off to the adaptive-learning
   service for the next-difficulty recommendation.
"""

from __future__ import annotations

import json
import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.ai.llm_provider import get_llm_provider
from app.ai.mcq_generator import GeneratedMCQ, RetrievedChunk, generate_demo_mcqs, generate_llm_mcqs
from app.ai.rag import get_rag_pipeline
from app.core.config import get_settings
from app.data.demo_data import generate_generic_quiz
from app.models.assessment import Assessment, AssessmentAttempt, Question
from app.models.competency import CompetencyScore
from app.models.employee import Employee
from app.models.material import DocumentChunk, LearningMaterial
from app.schemas.assessment import CompetencyImpact, PerQuestionResult
from app.services.adaptive_learning import next_difficulty_for_score
from app.services.competency_engine import latest_skill_levels
from app.services.skill_gap_engine import compute_skill_gaps, persist_skill_gaps

settings = get_settings()


def generate_assessment(
    db: Session,
    *,
    material_id: Optional[str],
    competency: str,
    domain: str,
    num_questions: int,
    difficulty: str,
    employee_id: Optional[str] = None,
) -> Assessment:
    generated_by = "demo"
    questions_data: List[GeneratedMCQ] = []
    source_label = "Generic competency self-check"

    if material_id:
        material = db.query(LearningMaterial).filter(LearningMaterial.id == material_id).first()
        if not material:
            raise ValueError(f"Learning material '{material_id}' not found.")
        if material.status != "ready":
            raise ValueError(f"Learning material '{material_id}' is not ready yet (status={material.status}).")
        source_label = material.original_filename

        rag = get_rag_pipeline()
        retrieved = rag.retrieve(f"{competency} {domain}", material_id=material_id, top_k=max(num_questions, 4))
        if not retrieved:
            # fall back to reading chunks straight from SQL if the vector store has nothing
            rows = (
                db.query(DocumentChunk)
                .filter(DocumentChunk.material_id == material_id)
                .order_by(DocumentChunk.chunk_index)
                .limit(max(num_questions, 4))
                .all()
            )
            retrieved = [{"chunk_id": r.id, "text": r.text} for r in rows]
        chunks = [RetrievedChunk(chunk_id=r["chunk_id"], text=r["text"]) for r in retrieved]
        if not chunks:
            raise ValueError("No extractable content found for this material yet.")

        if settings.DEMO_MODE:
            questions_data = generate_demo_mcqs(
                chunks, competency=competency, difficulty=difficulty, num_questions=num_questions,
                source_label=source_label,
            )
        else:
            llm = get_llm_provider()
            questions_data = generate_llm_mcqs(
                llm, chunks, competency=competency, difficulty=difficulty, num_questions=num_questions,
                source_label=source_label,
            )
            generated_by = "llm"
    else:
        raw = generate_generic_quiz(competency, domain, difficulty, num_questions)
        questions_data = [
            GeneratedMCQ(
                question=q["question"],
                options=q["options"],
                correct_answer=q["correct_answer"],
                explanation=q["explanation"],
                source_chunk_id=None,
            )
            for q in raw
        ]

    assessment_id = f"asmt_{uuid.uuid4().hex[:12]}"
    title = f"{competency} Assessment ({difficulty})"
    assessment = Assessment(
        id=assessment_id,
        title=title,
        competency_domain=domain,
        competency_skill=competency,
        difficulty=difficulty,
        material_id=material_id,
        generated_by=generated_by,
        created_for_employee=employee_id,
    )
    db.add(assessment)
    for i, q in enumerate(questions_data):
        db.add(
            Question(
                id=f"q_{uuid.uuid4().hex[:12]}",
                assessment_id=assessment_id,
                order_index=i,
                question=q.question,
                options=json.dumps(q.options),
                correct_answer=q.correct_answer,
                explanation=q.explanation,
                competency=competency,
                difficulty=difficulty,
                source=source_label,
                source_chunk_id=q.source_chunk_id,
            )
        )
    db.commit()
    db.refresh(assessment)
    return assessment


def evaluate_assessment(
    db: Session,
    *,
    assessment_id: str,
    employee_id: str,
    answers: dict[str, int],
) -> dict:
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise ValueError(f"Assessment '{assessment_id}' not found.")
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise ValueError(f"Employee '{employee_id}' not found.")

    questions = assessment.questions
    results: List[PerQuestionResult] = []
    correct_count = 0
    for q in questions:
        chosen = answers.get(q.id)
        is_correct = chosen is not None and chosen == q.correct_answer
        if is_correct:
            correct_count += 1
        results.append(
            PerQuestionResult(
                question_id=q.id,
                question=q.question,
                correct=is_correct,
                chosen_index=chosen,
                correct_index=q.correct_answer,
                explanation=q.explanation,
                competency=q.competency,
            )
        )

    total = len(questions)
    percentage = round((correct_count / total) * 100, 1) if total else 0.0

    # --- Deterministic competency update -------------------------------
    skill = assessment.competency_skill
    domain = assessment.competency_domain
    before_levels = latest_skill_levels(db, employee_id)
    before = before_levels.get(skill, {}).get("level", 0.0)

    new_evidence_level = round(1 + 4 * (percentage / 100.0), 2)
    if before > 0:
        w = settings.COMPETENCY_UPDATE_WEIGHT
        after = round(before * (1 - w) + new_evidence_level * w, 2)
    else:
        after = new_evidence_level
    after = max(1.0, min(5.0, after))

    db.add(
        CompetencyScore(
            employee_id=employee_id,
            domain=domain,
            skill=skill,
            level=after,
            source="assessment",
        )
    )
    db.commit()

    # --- Recompute skill gaps for the whole profile ---------------------
    db.refresh(employee)
    gaps = compute_skill_gaps(db, employee)
    persist_skill_gaps(db, employee_id, gaps)
    new_gap_skills = [g.skill for g in gaps if g.skill == skill]

    next_difficulty = next_difficulty_for_score(percentage)

    feedback = (
        f"You scored {correct_count}/{total} ({percentage:.0f}%) on {skill}. "
        f"Your estimated competency moved from {before:.1f}/5 to {after:.1f}/5. "
    )
    if percentage < settings.ADAPTIVE_EASY_MAX_PCT:
        feedback += "We recommend reinforcement material at an easier level before re-attempting."
    elif percentage < settings.ADAPTIVE_INTERMEDIATE_MAX_PCT:
        feedback += "Solid progress - intermediate-level material is recommended next."
    else:
        feedback += "Strong performance - you're ready for advanced material in this skill."

    attempt_id = f"attempt_{uuid.uuid4().hex[:12]}"
    db.add(
        AssessmentAttempt(
            id=attempt_id,
            assessment_id=assessment_id,
            employee_id=employee_id,
            answers_json=json.dumps(answers),
            score=correct_count,
            total=total,
            percentage=percentage,
            competency_before=before,
            competency_after=after,
            feedback=feedback,
            next_difficulty=next_difficulty,
        )
    )
    db.commit()

    return {
        "attempt_id": attempt_id,
        "assessment_id": assessment_id,
        "employee_id": employee_id,
        "score": correct_count,
        "total": total,
        "percentage": percentage,
        "correct_count": correct_count,
        "incorrect_count": total - correct_count,
        "results": results,
        "competency_impact": [
            CompetencyImpact(skill=skill, domain=domain, before=before, after=after, delta=round(after - before, 2))
        ],
        "feedback": feedback,
        "next_recommended_difficulty": next_difficulty,
        "new_skill_gaps": new_gap_skills,
    }
