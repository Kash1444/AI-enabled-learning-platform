# AI-enabled Learning Platform — AI Backend

AI/ML layer for **Smart India Hackathon 2026, Problem Statement 26101**
("Develop an AI enabled learning platform that identifies competency
gaps, recommends personalized training through integration with iGOT
Karmayogi, and generates quizzes/MCQs from uploaded learning materials"),
built for the Ministry of Statistics and Programme Implementation (MoSPI),
Data Informatics & Innovation Division (DIID).

This backend is **additive** — it does not modify, rename, or replace any
existing frontend file. It is consumed by the existing React frontend
through the service files already present in `frontend/src/services/`
(see section 14).

---

## 1. What this backend does

It implements the full "learning intelligence loop" described in the
problem statement — not a chatbot bolted onto static data:

```
Employee Profile → Competency Assessment → Competency Scores → Skill Gap
Analysis → Personalized Recommendations (iGOT/NSSTA) → Learning →
AI-generated Assessment → Assessment Result → Updated Competency →
Updated Skill Gaps → New Recommendations
```

Concretely, it provides:

- A **deterministic competency scoring engine** (never "ask an LLM for a
  number") producing explainable 1–5 competency levels per skill.
- A **skill-gap engine** comparing current vs. role-required levels with
  configurable priority thresholds.
- A **recommendation engine** that ranks iGOT-style and NSSTA-style
  resources against skill-gap severity, priority, level match and role
  relevance.
- A **RAG pipeline** (extraction → chunking → embeddings → ChromaDB →
  retrieval) over trainer-uploaded PDF/DOCX/PPTX/TXT materials.
- A **grounded MCQ generator** that only produces questions supported by
  the retrieved material (LLM-assisted when configured, with a
  zero-hallucination deterministic fallback always available).
- An **adaptive learning loop**: each quiz attempt updates the learner's
  competency estimate, recomputes skill gaps, and recommends the next
  quiz's difficulty.
- An **AI learning assistant** that routes between RAG-grounded answers,
  direct profile lookups, and general guidance — instead of always
  guessing.
- A full **DEMO_MODE** so every one of the above works with **zero**
  external credentials, for a demo that can't fail due to a flaky network
  or missing API key.

---

## 2. Architecture

```
                        React Frontend (unmodified)
                                   │
                                   ▼
                            FastAPI (app/main.py)
                                   │
      ┌───────────────┬───────────┼────────────────┬─────────────────┐
      ▼               ▼           ▼                ▼                 ▼
Competency        Skill Gap   Recommendation    Assessment        Assistant
Engine            Engine      Engine            Engine            Service
      │               │           │                │                 │
      │               │           ▼                ▼                 ▼
      │               │      iGOT / NSSTA      RAG Pipeline    RAG Pipeline
      │               │      Providers          (Chroma)        + Profile
      │               │      (mock/real)              │              lookup
      │               │                               ▼
      │               │                          LLM Provider
      │               │                     (Demo / Claude / OpenAI)
      ▼               ▼
     SQLite database (SQLAlchemy) — employees, roles, competency scores,
     skill gaps, materials, chunks, assessments, questions, attempts
```

Every box with a "mock/real" or "Demo/Claude/OpenAI" label is an **abstraction**
(`app/ai/llm_provider.py`, `app/ai/embeddings.py`,
`app/integrations/{igot,nssta}.py`) — swapping in real credentials never
requires touching the engines above them.

---

## 3. AI pipeline (RAG + MCQ generation)

```
Uploaded file (PDF/DOCX/PPTX/TXT)
        │  app/processors/document_processor.py
        ▼
  extract_text() → clean_text() → chunk_text()
        │
        ▼
  DocumentChunk rows (SQL, source of truth for citations)
        │  app/ai/embeddings.py
        ▼
  Embeddings (sentence-transformers, or offline hash fallback)
        │  app/ai/rag.py
        ▼
  ChromaDB persistent collection (storage/chroma/)
        │  RAGPipeline.retrieve(query, material_id)
        ▼
  Relevant chunks
        │  app/ai/mcq_generator.py
        ▼
  Grounded MCQs (LLM-assisted + Pydantic-validated, OR deterministic
  extractive generator in DEMO_MODE — the answer and every distractor are
  lifted verbatim from the material, so nothing is hallucinated)
```

---

## 4. Project structure

```
ai-backend/
├── app/
│   ├── main.py                     FastAPI app, CORS, exception handlers
│   ├── api/                        competency.py, recommendations.py,
│   │                               materials.py, assessments.py, assistant.py
│   ├── core/                       config.py, database.py, security.py
│   ├── models/                     SQLAlchemy ORM models
│   ├── schemas/                    Pydantic request/response models
│   ├── services/                   competency/skill-gap/recommendation/
│   │                               assessment/adaptive-learning/assistant engines
│   ├── ai/                         llm_provider.py, embeddings.py, rag.py,
│   │                               mcq_generator.py
│   ├── integrations/               base.py, igot.py, nssta.py (mock + real placeholder)
│   ├── processors/                 document_processor.py
│   └── data/                       competencies.py, roles.py, demo_data.py
├── storage/
│   ├── uploads/                    uploaded files land here
│   └── chroma/                     ChromaDB persistent store
├── tests/                          pytest suite (no API key required)
├── requirements.txt                full install (RAG + LLM SDKs)
├── requirements-minimal.txt        lightweight offline-only install
├── .env.example
├── .gitignore
├── run.py                          start the server (reads HOST/PORT)
├── seed.py                         load demo employees/roles/competencies
├── smoke_test.py                   end-to-end check vs a running server
└── README.md
```

---

## 5–11. Installation (Windows 11 / PowerShell)

### Prerequisites
- **Python 3.11 – 3.14** (verified on 3.14 / Windows 11)
- Git (to clone/pull the repo you already have)

### Step by step

```powershell
cd AI-enabled-learning-platform\ai-backend

# 1. Create a virtual environment
python -m venv .venv

# 2. Activate it
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
# --- OR, for a faster, fully-offline install with no LLM SDKs ---
# pip install -r requirements-minimal.txt

# 4. Configure environment variables
copy .env.example .env
# Defaults work out of the box. Change PORT here if 8000 is taken.

# 5. Seed demo data (3 employees, roles, competency scores, skill gaps)
python seed.py

# 6. Start the API
python run.py          # reads HOST/PORT from .env
# (equivalent to: uvicorn app.main:app --reload)
```

The API is now running at **http://localhost:8000** —
docs at **http://localhost:8000/docs**.

Then verify it end to end, with the server still running:

```powershell
python smoke_test.py   # drives every endpoint the React frontend calls
pytest -q              # unit + integration suite
```

> **VS Code**: select `ai-backend/.venv` as the interpreter
> (Ctrl+Shift+P → "Python: Select Interpreter"), otherwise the editor
> reports the installed packages as missing.

### A note on embeddings

`sentence-transformers` is **optional** and is not installed by default: it
requires torch, which has no Python 3.14 wheels yet. Without it,
`EMBEDDING_PROVIDER=auto` falls back to the dependency-free hashing
embedder, and RAG works end to end — retrieval ranking is just less
semantic. On Python ≤ 3.12, uncomment the pinned line in
`requirements.txt` for better retrieval quality.

If you installed `requirements-minimal.txt`, set `EMBEDDING_PROVIDER=hash`
in `.env` to skip the import attempt entirely.

---

## 10. DEMO_MODE

`DEMO_MODE=true` (the default) makes **every** feature work with zero
external credentials:

| Feature                     | DEMO_MODE=true                                   | DEMO_MODE=false (LLM configured)         |
|------------------------------|---------------------------------------------------|--------------------------------------------|
| Competency scoring            | Deterministic formula (always identical either way) | Same deterministic formula                |
| Skill gap analysis             | Deterministic thresholds (always identical either way) | Same                                       |
| Recommendations                | Ranked from mock iGOT/NSSTA data                   | Ranked from real providers if configured   |
| MCQ generation (with material) | Extractive, zero-hallucination generator            | LLM-grounded, falls back to extractive on any validation failure |
| MCQ generation (no material)   | Catalog-derived domain-membership quiz              | Same                                        |
| AI Assistant (with material)    | Extractive answer quoted from the retrieved chunks, with citations | Real LLM answer, still RAG-grounded and cited |
| AI Assistant (profile question) | Answered from the deterministic engines (identical either way) | Same |

To switch on real LLM generation, set in `.env`:

```env
DEMO_MODE=false
LLM_PROVIDER=anthropic     # or: openai
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-sonnet-5
```

A missing key, an uninstalled SDK, or an unrecognised `LLM_PROVIDER` logs a
warning and falls back to the offline provider rather than taking the API
down — a demo never dies because of a credential problem.

---

## 12. API documentation

Once running:
- Swagger UI: **http://localhost:8000/docs**
- ReDoc: **http://localhost:8000/redoc**

### Endpoint summary

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | Health check, reports DEMO_MODE |
| POST | `/api/competency/assess` | Score assessment answers deterministically |
| GET | `/api/competency/{employee_id}` | Competency overview (overall %, domains) |
| GET | `/api/competency/{employee_id}/gaps` | Skill gap analysis |
| GET | `/api/recommendations/{employee_id}` | Ranked personalized recommendations |
| GET | `/api/recommendations/{employee_id}/igot` | iGOT-style course recommendations |
| GET | `/api/recommendations/{employee_id}/nssta` | NSSTA-style program recommendations |
| POST | `/api/materials/upload` | Upload PDF/DOCX/PPTX/TXT (multipart) |
| GET | `/api/materials` | List uploaded materials |
| GET | `/api/materials/{material_id}` | Material detail + chunk preview |
| POST | `/api/assessment/generate` | Generate an MCQ assessment |
| GET | `/api/assessment/{assessment_id}` | Get assessment for a learner (no answer key) |
| POST | `/api/assessment/evaluate` | Submit answers, get score + updated competency |
| POST | `/api/assistant/chat` | Chat with the AI learning assistant |

### Example requests

**Assess competency**
```http
POST /api/competency/assess
Content-Type: application/json

{
  "employee_id": "EMP001",
  "answers": [
    {"question_id": "q1", "skill": "Python", "domain": "Technical",
     "difficulty": "Intermediate", "is_correct": true, "weight": 1.0}
  ]
}
```

**Get skill gaps**
```http
GET /api/competency/EMP001/gaps
```
```json
{
  "employee_id": "EMP001",
  "total_gaps": 5,
  "high_priority_gaps": 0,
  "medium_priority_gaps": 3,
  "low_priority_gaps": 2,
  "total_competency_gap": 4.1,
  "gaps": [
    {
      "id": 1, "skill": "Sampling Methodology", "domain": "Statistical",
      "current": 2.8, "required": 4.2, "gap": 1.4, "priority": "Medium",
      "description": "The learner demonstrated a competency level of 2.8/5 in Sampling Methodology, which is below the 4.2/5 required for the Statistical Officer role.",
      "recommendedAction": "Schedule a learning module on Sampling Methodology in your current learning path."
    }
  ]
}
```

**Upload a material**
```http
POST /api/materials/upload
Content-Type: multipart/form-data

file=<binary>, title="Sampling Methodology Notes",
competency_domain=Statistical, competency_skill=Sampling Methodology
```

**Generate a grounded assessment**
```http
POST /api/assessment/generate
Content-Type: application/json

{
  "material_id": "mat_a698a1079174",
  "competency": "Sampling Methodology",
  "domain": "Statistical",
  "num_questions": 5,
  "difficulty": "Intermediate"
}
```

**Chat with the assistant**
```http
POST /api/assistant/chat
Content-Type: application/json

{"employee_id": "EMP001", "message": "What are my biggest skill gaps?"}
```

---

## 13. Running tests

```powershell
.venv\Scripts\activate
pytest -q
```

All 40 tests pass **without any API key**: DEMO_MODE and the hash
embedding provider are forced on in `tests/conftest.py`, and a temporary
SQLite database is used so your seeded/demo data is never touched.

Coverage includes: health check, deterministic competency scoring
(including reproducibility and difficulty weighting), skill-gap
priority thresholds and gap computation, MCQ schema validation
(Pydantic rejects malformed/duplicate/out-of-range questions), the full
generate→evaluate assessment flow (including that the learner-facing GET
never leaks the answer key), and document processing (TXT/DOCX/PPTX
extraction, cleaning, chunking).

`tests/test_mcq_quality.py`, `tests/test_rag_and_llm.py` and
`tests/test_assistant.py` additionally pin behaviour that has broken
before: chunks must never start mid-word (those fragments used to be
served to learners as answer options), generated questions must have
distinct stems, Chroma retrieval must work through the `embed_query()`
hook that chromadb 1.x requires, the assistant must answer RAG questions
by quoting the material instead of returning a placeholder, and an
unknown/unconfigured LLM provider must degrade to the offline provider
instead of erroring.

### Live end-to-end check

`pytest` drives the app in-process. To check the *deployed* wiring — port,
CORS, seed data, persisted vector store — run the smoke test against a
running server:

```powershell
python run.py          # terminal 1
python smoke_test.py   # terminal 2
```

It walks the same 14 endpoints the React pages call and exits non-zero on
any failure.

---

## 14. Frontend integration

The service layer is already in place at `frontend/src/services/`:

| File | Endpoints it wraps |
|---|---|
| `apiClient.js` | shared fetch wrapper, reads `VITE_API_URL` |
| `competencyService.js` | `/api/competency/*` |
| `courseService.js` | `/api/recommendations/*` |
| `assessmentService.js` | `/api/materials/*`, `/api/assessment/*` |
| `assistantService.js` | `/api/assistant/chat` |

`frontend/.env` points those at this backend:

```env
VITE_API_URL=http://localhost:8000
```

**The origin only — no `/api` suffix.** `apiClient.js` prefixes every path
with `/api` itself, so including it here produces `/api/api/...` and every
call 404s.

Start both servers:
```powershell
# Terminal 1
cd ai-backend
.venv\Scripts\activate
python run.py

# Terminal 2
cd frontend
npm run dev
```

CORS is pre-configured for `http://localhost:5173` (Vite's default dev
port) via `CORS_ORIGINS` in `.env`.

**The frontend does not currently call this backend at all.** The service
files above are complete, but `AIAssistant.jsx` and `GenerateAssessment.jsx`
— the only two pages that import them — are not registered in
`routes/AppRoutes.jsx`, so the bundler drops them and `apiClient.js` never
ships. Every other page renders the static fixtures in `frontend/src/data/`.

Nothing here needs to change to fix that; see "Frontend wiring status" in
the root [`README.md`](../README.md) for the exact list. The backend side is
verified independently by `smoke_test.py`.

---

## 15–19. Engine details

### RAG pipeline
`app/ai/rag.py` wraps a persistent ChromaDB collection (`storage/chroma/`)
behind `RAGPipeline.index_material()` / `.retrieve()`. Embeddings come
from `app/ai/embeddings.py`, which tries
`sentence-transformers/all-MiniLM-L6-v2` (configurable via
`EMBEDDING_MODEL`) and falls back to a dependency-free deterministic
hashing embedding if that package/model isn't available — so RAG never
hard-fails in an offline demo environment.

### MCQ generation
`app/ai/mcq_generator.py` validates every generated question with
Pydantic (`GeneratedMCQ`): exactly 4 unique options, a valid correct-answer
index. The LLM path asks for strict JSON and uses the LLM provider's own
repair loop on malformed output; if validation still fails, it
**automatically falls back** to the deterministic extractive generator
rather than ever returning a broken or unsupported question.

The deterministic generator builds **fill-in-the-blank** questions: it
picks the most distinctive term in a sentence (the one appearing in the
fewest other sentences), blanks it, and draws the three distractors from
terms elsewhere in the same document — skipping any that already appear in
the sentence or share a root with the answer. Each question therefore reads
differently and tests recall of the material rather than which of four
unrelated sentences came from the document. When a sentence has no
distinctive term to blank, it falls back to statement-selection. Output is
seeded from the material and competency, so the same upload always produces
the same quiz.

### Competency engine
`app/services/competency_engine.py` — see section 3 of this README and
the module's docstring: score = correctness × difficulty-weight × question
weight, mapped onto a 1–5 scale. 100% reproducible for the same answers.

### Skill gap engine
`app/services/skill_gap_engine.py` — `gap = required - current`,
priority via `GAP_HIGH_THRESHOLD` / `GAP_MEDIUM_THRESHOLD` (`.env`,
defaults 1.5 / 0.75). Every gap carries a generated `description` and
`recommendedAction` for explainability.

### Recommendation engine
`app/services/recommendation_engine.py` — ranks iGOT/NSSTA candidates
using gap severity (50%), priority weight (30%), and level match to the
learner's current stage (20%), fully documented and inspectable via each
result's `reason`.

### iGOT / NSSTA integration
`app/integrations/{igot,nssta}.py` — a `CourseProviderInterface` /
`ProgramProviderInterface` with a `Mock*Provider` (always available,
demo data clearly flagged `is_demo_data: true`) and a `Real*Provider`
placeholder that raises `NotImplementedError` with instructions, rather
than pretending to call a live government API without credentials. Wire
up `IGOT_API_BASE_URL` / `IGOT_API_KEY` (or the NSSTA equivalents) in
`.env` and implement the two methods in the `Real*Provider` class to go
live — nothing else in the codebase needs to change.

---

## 20. Future improvements

- Persist `LearningResource`/`Recommendation` rows to SQL instead of
  computing recommendations on the fly (already modeled in
  `app/models/recommendation.py`), enabling recommendation history/audit.
- Replace the static bearer-token auth abstraction (`app/core/security.py`)
  with real OAuth2/JWT once an identity provider is chosen.
- Add pagination to `/api/materials` and `/api/recommendations/*`.
- Add a background task queue (e.g. Celery/RQ) for large-file processing
  instead of processing uploads synchronously.
- Extend `document_processor.py` to support video transcripts (the
  architecture already isolates format-specific extraction).
- Migrate `DATABASE_URL` to PostgreSQL for multi-user concurrent access.

---

## Security notes (realistic, hackathon-appropriate)

- Secrets only ever come from environment variables (`.env`, never
  committed — see `.gitignore`).
- Uploaded filenames are sanitized and prefixed with a UUID
  (`app/core/security.py::safe_filename`); resolved paths are checked
  against path traversal (`resolve_within_upload_dir`).
- File type and size are validated before anything is written to disk.
- All unhandled exceptions are caught centrally in `app/main.py` and
  never leak stack traces to the client; details are logged locally.
- An optional static-bearer-token auth dependency
  (`API_AUTH_ENABLED`/`API_STATIC_TOKEN`) is provided as a placeholder —
  it is intentionally simple and documented as such, not a replacement
  for real auth in a production deployment.
