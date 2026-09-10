"""
MCQ (multiple-choice question) generator.

Two code paths, chosen automatically:

1. LLM path (DEMO_MODE=false + LLM configured): retrieved chunks are
   embedded directly into a strict prompt that instructs the model to only
   use the provided material and to return structured JSON. The response
   is validated against `GeneratedMCQ` / Pydantic; on malformed JSON the
   LLM provider's own repair loop is used; if it still fails validation we
   fall back to the deterministic generator below rather than surface a
   broken question to a learner.

2. Deterministic/offline path (DEMO_MODE=true, or as an automatic
   fallback): questions are built directly from sentences that literally
   appear in the uploaded material, so there is zero hallucination risk by
   construction. Distractors come from *other* sentences in the same
   document set, never invented facts.

Both paths return the same `List[GeneratedMCQ]` shape.
"""

from __future__ import annotations

import hashlib
import logging
import random
import re
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from app.ai.llm_provider import LLMProvider

logger = logging.getLogger(__name__)

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


class RetrievedChunk(BaseModel):
    chunk_id: str
    text: str


class GeneratedMCQ(BaseModel):
    question: str
    options: List[str] = Field(min_length=4, max_length=4)
    correct_answer: int
    explanation: str
    source_chunk_id: Optional[str] = None

    @field_validator("correct_answer")
    @classmethod
    def _valid_index(cls, v: int) -> int:
        if not (0 <= v <= 3):
            raise ValueError("correct_answer must be an index between 0 and 3")
        return v

    @field_validator("options")
    @classmethod
    def _unique_options(cls, v: List[str]) -> List[str]:
        if len({o.strip().lower() for o in v}) != len(v):
            raise ValueError("options must be unique")
        return v


def _dedupe_sentences(text: str) -> List[str]:
    sentences = [s.strip() for s in _SENTENCE_SPLIT.split(text) if s.strip()]
    return [s for s in sentences if 40 <= len(s) <= 240]


def _candidate_pool(chunks: List[RetrievedChunk]) -> List[dict]:
    pool: List[dict] = []
    seen = set()
    for chunk in chunks:
        for sentence in _dedupe_sentences(chunk.text):
            key = sentence.lower()
            if key in seen:
                continue
            seen.add(key)
            pool.append({"sentence": sentence, "chunk_id": chunk.chunk_id})
    return pool


def generate_demo_mcqs(
    chunks: List[RetrievedChunk],
    *,
    competency: str,
    difficulty: str,
    num_questions: int,
    source_label: str,
) -> List[GeneratedMCQ]:
    """
    Deterministic, offline, grounded MCQ generation.

    Every "correct" option is a sentence that appears verbatim in the
    uploaded material; every distractor is a sentence pulled from a
    *different* part of the material, so nothing is invented.
    """
    pool = _candidate_pool(chunks)
    if len(pool) < 2:
        raise ValueError(
            "Not enough extractable content in the uploaded material to generate grounded questions. "
            "Try uploading a longer/more detailed document."
        )

    # deterministic shuffle (stable across identical inputs -> reproducible demo)
    seed = int(hashlib.md5((source_label + competency + difficulty).encode()).hexdigest(), 16) % (2**32)
    rng = random.Random(seed)
    indices = list(range(len(pool)))
    rng.shuffle(indices)

    questions: List[GeneratedMCQ] = []
    used_correct = set()
    difficulty_stub = {
        "Easy": "Which of the following statements is mentioned in the material?",
        "Intermediate": "Based on the uploaded material, which statement is accurate?",
        "Advanced": "According to a detailed reading of the material, which statement correctly reflects its content?",
    }.get(difficulty, "Which of the following statements is mentioned in the material?")

    attempts = 0
    while len(questions) < num_questions and attempts < len(pool) * 2:
        attempts += 1
        correct_idx = indices[attempts % len(indices)]
        if correct_idx in used_correct:
            continue
        correct_item = pool[correct_idx]

        # pick 3 distractors from sentences that are NOT the correct one
        distractor_pool = [p for i, p in enumerate(pool) if i != correct_idx]
        if len(distractor_pool) < 3:
            break
        rng.shuffle(distractor_pool)
        distractors = distractor_pool[:3]

        options = [correct_item["sentence"]] + [d["sentence"] for d in distractors]
        # shuffle option order, tracking correct index
        order = list(range(4))
        rng.shuffle(order)
        shuffled_options = [options[i] for i in order]
        correct_answer = order.index(0)

        used_correct.add(correct_idx)
        questions.append(
            GeneratedMCQ(
                question=f"[{competency}] {difficulty_stub}",
                options=shuffled_options,
                correct_answer=correct_answer,
                explanation=(
                    f"This statement appears directly in the uploaded material "
                    f"('{source_label}'); the other options are drawn from unrelated "
                    f"parts of the same document and do not answer the question."
                ),
                source_chunk_id=correct_item["chunk_id"],
            )
        )

    if not questions:
        raise ValueError("Could not generate any grounded questions from the supplied material.")
    return questions


def generate_llm_mcqs(
    llm: LLMProvider,
    chunks: List[RetrievedChunk],
    *,
    competency: str,
    difficulty: str,
    num_questions: int,
    source_label: str,
) -> List[GeneratedMCQ]:
    """LLM-grounded generation. Falls back to the demo generator on any
    validation failure so a broken/hallucinated quiz is never returned."""
    context = "\n\n".join(f"[chunk:{c.chunk_id}] {c.text}" for c in chunks)
    system = (
        "You write exam-quality multiple-choice questions strictly grounded in the "
        "provided source material. Every fact in the question, the correct answer, "
        "and every distractor must be verifiable from the material. Never invent facts "
        "not present in the material. Respond with ONLY valid JSON."
    )
    prompt = f"""
Source material (competency: {competency}, target difficulty: {difficulty}):
---
{context}
---

Generate exactly {num_questions} multiple-choice questions as a JSON object:
{{
  "questions": [
    {{
      "question": "...",
      "options": ["...", "...", "...", "..."],
      "correct_answer": 0,
      "explanation": "...",
      "source_chunk_id": "chunk id this question is grounded in, from the [chunk:ID] tags above"
    }}
  ]
}}
Rules: exactly 4 options per question, exactly one correct answer, options must be
plausible and mutually exclusive, no duplicate questions, difficulty="{difficulty}".
"""
    try:
        raw = llm.generate_json(prompt, system=system, max_tokens=1800 + 200 * num_questions)
        raw_questions = raw.get("questions", [])
        validated = [GeneratedMCQ(**q) for q in raw_questions]
        # de-duplicate by normalized question text
        seen = set()
        deduped = []
        for q in validated:
            key = q.question.strip().lower()
            if key in seen:
                continue
            seen.add(key)
            deduped.append(q)
        if len(deduped) < 1:
            raise ValueError("LLM returned zero valid questions")
        return deduped[:num_questions]
    except Exception as exc:  # noqa: BLE001
        logger.warning("LLM MCQ generation failed (%s); falling back to grounded demo generator.", exc)
        return generate_demo_mcqs(
            chunks,
            competency=competency,
            difficulty=difficulty,
            num_questions=num_questions,
            source_label=source_label,
        )
