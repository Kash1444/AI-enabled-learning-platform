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


def _normalize_ws(text: str) -> str:
    """Collapse newlines/runs of whitespace so an option is always one line."""
    return re.sub(r"\s+", " ", text).strip()


def _dedupe_sentences(text: str) -> List[str]:
    """
    Split a chunk into sentences usable as quiz content.

    Chunks overlap, so the first sentence of a chunk may be the tail of a
    sentence that began in the previous one. Such fragments read as broken
    English ("ariance relative to simple random sampling...") and must never
    reach a learner as an answer option, so we require a sentence to begin
    the way a real sentence does.
    """
    sentences = [_normalize_ws(s) for s in _SENTENCE_SPLIT.split(text) if s.strip()]
    return [s for s in sentences if 40 <= len(s) <= 240 and _starts_like_a_sentence(s)]


def _starts_like_a_sentence(sentence: str) -> bool:
    first = sentence[0]
    return first.isupper() or first.isdigit() or first == "["


# Words too generic to make a fair cloze answer or a distinguishing distractor.
_STOPWORDS = {
    "about", "above", "after", "again", "against", "already", "also", "although",
    "always", "among", "because", "been", "before", "being", "below", "between",
    "both", "cannot", "could", "does", "doing", "during", "each", "either",
    "every", "from", "further", "have", "having", "here", "however", "into",
    "itself", "less", "like", "made", "make", "many", "more", "most", "much",
    "must", "only", "other", "others", "over", "rather", "same", "several",
    "should", "since", "some", "such", "than", "that", "their", "them", "then",
    "there", "these", "they", "this", "those", "through", "thus", "under",
    "until", "used", "using", "very", "were", "what", "when", "where", "which",
    "while", "with", "within", "without", "would", "your",
}

_WORD_RE = re.compile(r"[A-Za-z][A-Za-z\-]{3,}")


def _content_words(sentence: str) -> List[str]:
    return [w for w in _WORD_RE.findall(sentence) if w.lower() not in _STOPWORDS]


def _same_root(a: str, b: str) -> bool:
    """Cheap singular/plural + inflection guard ('stratum' vs 'strata' stays
    distinct, but 'sample' vs 'samples' collapses)."""
    a, b = a.lower(), b.lower()
    if a == b:
        return True
    return a[:5] == b[:5] and abs(len(a) - len(b)) <= 2


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


def _term_document_frequency(pool: List[dict]) -> dict:
    """How many sentences each content word appears in — used to pick the most
    *distinctive* term in a sentence as the cloze answer."""
    freq: dict = {}
    for item in pool:
        for word in {w.lower() for w in _content_words(item["sentence"])}:
            freq[word] = freq.get(word, 0) + 1
    return freq


def _pick_cloze_term(sentence: str, freq: dict) -> Optional[str]:
    """Pick the rarest (therefore most content-bearing) word in the sentence.
    Ties break toward the longer word, then alphabetically, so the choice is
    fully deterministic."""
    candidates = {w for w in _content_words(sentence) if len(w) >= 5}
    if not candidates:
        return None
    return sorted(candidates, key=lambda w: (freq.get(w.lower(), 0), -len(w), w.lower()))[0]


def _blank_out(sentence: str, term: str) -> str:
    """Replace the first whole-word occurrence of `term` with a blank."""
    return re.sub(rf"\b{re.escape(term)}\b", "______", sentence, count=1)


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

    freq = _term_document_frequency(pool)
    questions: List[GeneratedMCQ] = []
    used_correct: set = set()
    used_terms: List[str] = []

    for correct_idx in indices:
        if len(questions) >= num_questions:
            break
        if correct_idx in used_correct:
            continue
        correct_item = pool[correct_idx]
        used_correct.add(correct_idx)

        mcq = _build_cloze_question(
            pool,
            correct_idx,
            freq,
            rng,
            competency=competency,
            used_terms=used_terms,
        ) or _build_statement_question(
            pool,
            correct_idx,
            rng,
            competency=competency,
            difficulty=difficulty,
            source_label=source_label,
        )
        if mcq is not None:
            questions.append(mcq)

    if not questions:
        raise ValueError("Could not generate any grounded questions from the supplied material.")
    return questions


def _build_cloze_question(
    pool: List[dict],
    correct_idx: int,
    freq: dict,
    rng: random.Random,
    *,
    competency: str,
    used_terms: List[str],
) -> Optional[GeneratedMCQ]:
    """
    Build a fill-in-the-blank question.

    This tests whether the learner knows the key term rather than whether
    they can spot which of four unrelated sentences came from the document,
    and each question reads differently. The answer and every distractor are
    words lifted from the material, so nothing is invented.
    """
    sentence = pool[correct_idx]["sentence"]
    answer = _pick_cloze_term(sentence, freq)
    if not answer or any(_same_root(answer, t) for t in used_terms):
        return None

    # Distractors: terms from other sentences that are not the answer and do
    # not already appear in this sentence (which would make them defensible).
    seen_in_sentence = {w.lower() for w in _content_words(sentence)}
    candidates: List[str] = []
    for i, item in enumerate(pool):
        if i == correct_idx:
            continue
        for word in _content_words(item["sentence"]):
            if len(word) < 5 or word.lower() in seen_in_sentence:
                continue
            if _same_root(word, answer) or any(_same_root(word, c) for c in candidates):
                continue
            candidates.append(word)
    if len(candidates) < 3:
        return None

    rng.shuffle(candidates)
    options = [answer] + candidates[:3]
    order = list(range(4))
    rng.shuffle(order)
    shuffled = [options[i] for i in order]

    used_terms.append(answer)
    return GeneratedMCQ(
        question=f"[{competency}] Complete the statement from the material: \"{_blank_out(sentence, answer)}\"",
        options=shuffled,
        correct_answer=order.index(0),
        explanation=f'The material states: "{sentence}"',
        source_chunk_id=pool[correct_idx]["chunk_id"],
    )


def _build_statement_question(
    pool: List[dict],
    correct_idx: int,
    rng: random.Random,
    *,
    competency: str,
    difficulty: str,
    source_label: str,
) -> Optional[GeneratedMCQ]:
    """Fallback: pick the statement that genuinely comes from the material.
    Used when a sentence has no distinctive term to blank out."""
    correct_item = pool[correct_idx]
    distractor_pool = [p for i, p in enumerate(pool) if i != correct_idx]
    if len(distractor_pool) < 3:
        return None

    rng.shuffle(distractor_pool)
    distractors = distractor_pool[:3]
    options = [correct_item["sentence"]] + [d["sentence"] for d in distractors]
    if len({o.strip().lower() for o in options}) != 4:
        return None

    order = list(range(4))
    rng.shuffle(order)
    shuffled = [options[i] for i in order]

    stub = {
        "Easy": "Which of the following statements is mentioned in the material?",
        "Intermediate": "Based on the uploaded material, which statement is accurate?",
        "Advanced": "According to a detailed reading of the material, which statement correctly reflects its content?",
    }.get(difficulty, "Which of the following statements is mentioned in the material?")

    return GeneratedMCQ(
        question=f"[{competency}] {stub}",
        options=shuffled,
        correct_answer=order.index(0),
        explanation=(
            f"This statement appears directly in the uploaded material "
            f"('{source_label}'); the other options are drawn from unrelated "
            f"parts of the same document and do not answer the question."
        ),
        source_chunk_id=correct_item["chunk_id"],
    )


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
