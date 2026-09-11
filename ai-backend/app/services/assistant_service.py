"""
AI Learning Assistant service.

This is deliberately NOT "just a chatbot": incoming messages are routed
through one of three modes before anything is sent to an LLM.

    1. "rag"      - a `material_id` was supplied -> retrieve relevant
                     chunks from that material via the RAG pipeline and
                     ground the answer in them (with citations).
    2. "profile"  - the message looks like a question about the learner's
                     *own* competency/skill-gap/recommendation data (e.g.
                     "what are my biggest skill gaps?") -> answer directly
                     from the deterministic engines/DB, no LLM guessing.
    3. "general"  - anything else -> a general answer, explicitly avoiding
                     unsupported government-specific claims, using the
                     configured LLM provider (or the offline demo provider).
"""

from __future__ import annotations

import re
from typing import List

from sqlalchemy.orm import Session

from app.ai.llm_provider import DemoLLMProvider, get_llm_provider
from app.ai.rag import get_rag_pipeline
from app.models.employee import Employee
from app.models.material import LearningMaterial
from app.schemas.assistant import ChatResponse, SourceRef
from app.services.skill_gap_engine import compute_skill_gaps

_PROFILE_PATTERNS = [
    r"skill gap",
    r"competenc",
    r"my (score|level|progress)",
    r"what should i learn",
    r"recommend",
]


def _looks_like_profile_question(message: str) -> bool:
    text = message.lower()
    return any(re.search(p, text) for p in _PROFILE_PATTERNS)


def _answer_from_profile(db: Session, employee: Employee) -> str:
    gaps = compute_skill_gaps(db, employee)
    if not gaps:
        return (
            f"Based on your current competency profile, you have no significant skill gaps "
            f"relative to the requirements of your role. Great work - consider exploring "
            f"advanced modules to keep growing."
        )
    top = gaps[:3]
    lines = [
        f"Here's what your competency profile shows, {employee.name.split()[0] if employee.name else 'there'}:",
        "",
    ]
    for g in top:
        lines.append(
            f"- {g.skill} ({g.domain}): current {g.current:.1f}/5, required {g.required:.1f}/5, "
            f"gap {g.gap:.1f} — {g.priority} priority. {g.recommended_action}"
        )
    lines.append("")
    lines.append(
        f"In total you have {len(gaps)} identified skill gap(s). The highest-priority one is "
        f"'{top[0].skill}' — closing this would have the biggest impact on meeting your role's "
        f"competency requirements."
    )
    return "\n".join(lines)


def _answer_with_rag(db: Session, message: str, material_id: str) -> tuple[str, List[SourceRef], bool]:
    material = db.query(LearningMaterial).filter(LearningMaterial.id == material_id).first()
    if not material:
        return (
            f"I couldn't find a learning material with id '{material_id}'. "
            f"Please check the material was uploaded and finished processing.",
            [],
            False,
        )
    rag = get_rag_pipeline()
    hits = rag.retrieve(message, material_id=material_id, top_k=4)
    if not hits:
        return (
            f"I couldn't find any relevant content in '{material.title}' for that question. "
            f"Try rephrasing, or ask a more general question.",
            [],
            False,
        )

    context = "\n\n".join(f"[{i+1}] {h['text']}" for i, h in enumerate(hits))
    llm = get_llm_provider()

    # The offline demo provider cannot read `context`, so asking it to answer
    # would return a generic placeholder and make a working retrieval look
    # broken. Answer extractively from the retrieved chunks instead: the text
    # is quoted from the material, so it stays grounded and citable.
    if isinstance(llm, DemoLLMProvider):
        return _extractive_answer(message, hits, material.title), _build_sources(material, hits), True

    system = (
        "You are a learning assistant for India's Official Statistical System. Answer the "
        "learner's question using ONLY the provided source material excerpts. If the "
        "excerpts do not contain the answer, say so plainly instead of guessing. Do not "
        "make unsupported claims about government policy, schemes, or procedures beyond "
        "what the material states."
    )
    prompt = f"Source material excerpts:\n{context}\n\nLearner question: {message}\n\nAnswer:"
    answer = llm.generate(prompt, system=system, max_tokens=600)
    return answer, _build_sources(material, hits), True


def _build_sources(material: LearningMaterial, hits: List[dict]) -> List[SourceRef]:
    return [
        SourceRef(
            material_id=material.id,
            material_title=material.title,
            chunk_id=h["chunk_id"],
            text_preview=(h["text"][:220] + ("..." if len(h["text"]) > 220 else "")),
        )
        for h in hits
    ]


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_QUERY_STOPWORDS = {
    "what", "which", "when", "where", "does", "do", "is", "are", "the", "a",
    "an", "of", "for", "in", "on", "to", "and", "or", "how", "why", "can",
    "explain", "tell", "me", "about", "that", "this", "it",
}


def _extractive_answer(message: str, hits: List[dict], material_title: str) -> str:
    """
    Answer a question using only sentences that appear in the retrieved
    chunks, ranked by overlap with the learner's question.

    This is deliberately extractive rather than generative: in DEMO_MODE
    there is no language model available, and quoting the material is both
    honest and verifiable against the citations returned alongside it.
    """
    query_terms = {
        w for w in re.findall(r"[a-z][a-z\-]{2,}", message.lower()) if w not in _QUERY_STOPWORDS
    }

    scored: List[tuple] = []
    seen: set = set()
    for hit in hits:
        for raw in _SENTENCE_SPLIT.split(hit["text"]):
            sentence = re.sub(r"\s+", " ", raw).strip()
            if len(sentence) < 40 or sentence.lower() in seen:
                continue
            seen.add(sentence.lower())
            words = set(re.findall(r"[a-z][a-z\-]{2,}", sentence.lower()))
            overlap = len(query_terms & words)
            if overlap:
                scored.append((overlap, -len(sentence), sentence))

    if not scored:
        return (
            f"I found relevant sections in '{material_title}' but nothing that directly "
            f"answers that question. The cited excerpts below are the closest matches — "
            f"try rephrasing using terms from the material."
        )

    scored.sort(reverse=True)
    best = [s for _, _, s in scored[:3]]
    body = "\n".join(f"- {s}" for s in best)
    return (
        f"Here is what '{material_title}' says about that:\n\n{body}\n\n"
        f"(Answered by quoting the uploaded material directly — DEMO_MODE is on, so no "
        f"language model was used to rephrase it. Sources are cited below.)"
    )


def _answer_generally(message: str) -> str:
    llm = get_llm_provider()
    if isinstance(llm, DemoLLMProvider):
        return (
            "I can answer two kinds of question with real data in this demo:\n\n"
            "- **Your own profile** — ask about your competencies, skill gaps, scores or "
            "what you should learn next, and I'll answer from your assessment results.\n"
            "- **An uploaded material** — open a learning material and ask about its "
            "content, and I'll answer using retrieval over that document, with citations.\n\n"
            "For open-ended questions outside those two, a language model is needed. "
            "DEMO_MODE is currently on, so no model is configured — set `DEMO_MODE=false` "
            "with an API key in the backend `.env` to enable free-form answers."
        )
    system = (
        "You are a learning assistant for India's Official Statistical System training "
        "platform. Give helpful, general study guidance. Do NOT state specific facts about "
        "government schemes, iGOT Karmayogi content, or NSSTA programs beyond generic, "
        "clearly-labelled examples, since you do not have a live connection to those systems "
        "in this conversation."
    )
    return llm.generate(message, system=system, max_tokens=500)


def chat(db: Session, *, employee_id: str, message: str, material_id: str | None) -> ChatResponse:
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if material_id:
        answer, sources, used_rag = _answer_with_rag(db, message, material_id)
        return ChatResponse(answer=answer, sources=sources, used_rag=used_rag, mode="rag")

    if employee and _looks_like_profile_question(message):
        answer = _answer_from_profile(db, employee)
        return ChatResponse(answer=answer, sources=[], used_rag=False, mode="profile")

    answer = _answer_generally(message)
    return ChatResponse(answer=answer, sources=[], used_rag=False, mode="general")
