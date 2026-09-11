"""
End-to-end smoke test against a RUNNING server.

Unlike `pytest` (which exercises the app in-process with a throwaway
database), this drives the real HTTP API exactly as the React frontend
does — same paths, same payload shapes as frontend/src/services/*.js — so
it catches wiring problems the unit tests cannot: a wrong port, CORS,
missing seed data, or a vector store that failed to persist.

    python run.py          # terminal 1
    python smoke_test.py   # terminal 2

Exits non-zero if any check fails.
"""

from __future__ import annotations

import io
import json
import sys
import urllib.error
import urllib.request
import uuid

from app.core.config import get_settings

settings = get_settings()
BASE = f"http://{settings.HOST}:{settings.PORT}"
EMPLOYEE = "EMP001"

_passed = 0
_failed: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    global _passed
    if condition:
        _passed += 1
        print(f"  PASS  {name}")
    else:
        _failed.append(name)
        print(f"  FAIL  {name} {detail}")


def get(path: str):
    with urllib.request.urlopen(BASE + path, timeout=60) as response:
        return json.load(response)


def post(path: str, body: dict):
    request = urllib.request.Request(
        BASE + path,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.load(response)


def upload(path: str, filename: str, content: bytes, fields: dict):
    """Minimal multipart/form-data encoder (no extra dependency needed)."""
    boundary = f"----smoke{uuid.uuid4().hex}"
    buffer = io.BytesIO()
    for key, value in fields.items():
        buffer.write(f"--{boundary}\r\n".encode())
        buffer.write(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode())
        buffer.write(f"{value}\r\n".encode())
    buffer.write(f"--{boundary}\r\n".encode())
    buffer.write(
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode()
    )
    buffer.write(b"Content-Type: text/plain\r\n\r\n")
    buffer.write(content)
    buffer.write(f"\r\n--{boundary}--\r\n".encode())

    request = urllib.request.Request(
        BASE + path,
        data=buffer.getvalue(),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.load(response)


SAMPLE = b"""Sampling Methodology for Official Statistics

Simple random sampling is a technique in which every unit in the population has an equal and known probability of being selected.

Stratified sampling divides the population into homogeneous subgroups called strata, and then draws an independent sample from each stratum.

Cluster sampling selects groups of units, known as clusters, rather than individual units. It reduces travel and listing costs in large-scale household surveys.

Systematic sampling selects every kth unit from an ordered list after a random start.

The design effect measures the ratio of the variance under the actual complex sample design to the variance under simple random sampling of the same size.

Non-sampling errors include coverage errors, non-response errors, measurement errors and processing errors.

The sampling frame is the list of units from which the sample is actually drawn.
"""


def main() -> int:
    print(f"Smoke testing {BASE}\n")

    print("health")
    health = get("/api/health")
    check("GET /api/health", health.get("status") == "ok", health)

    print("\ncompetency (Competencies.jsx, SkillGaps.jsx)")
    competency = get(f"/api/competency/{EMPLOYEE}")
    check("GET /api/competency/{id}", competency.get("employee_id") == EMPLOYEE)
    check("  has domain breakdown", bool(competency.get("domains")))
    check("  overall % is sane", 0 <= competency.get("overall_competency_pct", -1) <= 100)

    gaps = get(f"/api/competency/{EMPLOYEE}/gaps")
    check("GET /api/competency/{id}/gaps", "gaps" in gaps)
    check("  gap rows carry explanations", all(g.get("description") for g in gaps["gaps"]))

    scored = post(
        "/api/competency/assess",
        {
            "employee_id": EMPLOYEE,
            "answers": [
                {
                    "question_id": "q1",
                    "skill": "Python",
                    "domain": "Technical",
                    "difficulty": "Intermediate",
                    "is_correct": True,
                    "weight": 1.0,
                }
            ],
        },
    )
    check("POST /api/competency/assess", scored.get("employee_id") == EMPLOYEE)

    print("\nrecommendations (LearningPath.jsx, IGOTCourses.jsx, NSSTAPrograms.jsx)")
    recs = get(f"/api/recommendations/{EMPLOYEE}?limit=5")
    check("GET /api/recommendations/{id}", bool(recs.get("recommendations")))
    check("  every item explains itself", all(r.get("reason") for r in recs["recommendations"]))

    igot = get(f"/api/recommendations/{EMPLOYEE}/igot")
    check("GET /api/recommendations/{id}/igot", "courses" in igot)
    check("  demo data is flagged", igot.get("source") in ("mock", "live"))

    nssta = get(f"/api/recommendations/{EMPLOYEE}/nssta")
    check("GET /api/recommendations/{id}/nssta", "programs" in nssta)

    print("\nmaterials (UploadMaterials.jsx)")
    material = upload(
        "/api/materials/upload",
        "smoke_sampling.txt",
        SAMPLE,
        {
            "title": "Smoke Test Sampling Notes",
            "competency_domain": "Statistical",
            "competency_skill": "Sampling Methodology",
            "uploaded_by": "smoke_test",
        },
    )
    material_id = material.get("id")
    check("POST /api/materials/upload", material.get("status") == "ready", material)
    check("  text was chunked", material.get("chunk_count", 0) > 0)

    listing = get("/api/materials")
    check("GET /api/materials", any(m["id"] == material_id for m in listing["materials"]))
    check("GET /api/materials/{id}", get(f"/api/materials/{material_id}")["id"] == material_id)

    print("\nassessment (GenerateAssessment.jsx, Quiz.jsx, QuizResult.jsx)")
    generated = post(
        "/api/assessment/generate",
        {
            "material_id": material_id,
            "competency": "Sampling Methodology",
            "domain": "Statistical",
            "num_questions": 4,
            "difficulty": "Intermediate",
            "employee_id": EMPLOYEE,
        },
    )
    questions = generated.get("questions", [])
    check("POST /api/assessment/generate", len(questions) > 0)
    check("  grounded in the uploaded material", generated.get("material_id") == material_id)
    check("  question stems are distinct", len({q["question"] for q in questions}) == len(questions))
    check(
        "  options are single-line and non-empty",
        all(o.strip() and "\n" not in o for q in questions for o in q["options"]),
    )

    learner_view = get(f"/api/assessment/{generated['id']}")
    check(
        "GET /api/assessment/{id} withholds the answer key",
        all("correct_answer" not in q for q in learner_view["questions"]),
    )

    result = post(
        "/api/assessment/evaluate",
        {
            "assessment_id": generated["id"],
            "employee_id": EMPLOYEE,
            "answers": {q["id"]: q["correct_answer"] for q in questions},
        },
    )
    check("POST /api/assessment/evaluate", result.get("percentage") == 100.0, result.get("percentage"))
    check("  competency was updated by the attempt", bool(result.get("competency_impact")))
    check("  next difficulty suggested", bool(result.get("next_recommended_difficulty")))

    print("\nassistant (AIAssistant.jsx)")
    rag = post(
        "/api/assistant/chat",
        {
            "employee_id": EMPLOYEE,
            "message": "What is the design effect?",
            "material_id": material_id,
        },
    )
    check("POST /api/assistant/chat (rag)", rag.get("mode") == "rag")
    check("  answer is cited", bool(rag.get("sources")))
    check("  answer is grounded, not a placeholder", "design effect" in rag["answer"].lower())

    profile = post(
        "/api/assistant/chat",
        {"employee_id": EMPLOYEE, "message": "What are my biggest skill gaps?"},
    )
    check("POST /api/assistant/chat (profile)", profile.get("mode") == "profile")

    print(f"\n{_passed} passed, {len(_failed)} failed")
    if _failed:
        for name in _failed:
            print(f"  - {name}")
        return 1
    print("All frontend-facing endpoints are working.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except urllib.error.URLError as exc:
        print(f"\nCould not reach {BASE}: {exc}")
        print("Start the server first:  python run.py")
        sys.exit(2)
