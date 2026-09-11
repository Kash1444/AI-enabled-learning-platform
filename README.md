# AI-Enabled Learning Platform

An AI-powered learning and skill intelligence platform developed for **Smart India Hackathon (SIH) 2026** under Problem Statement **26101** by the **Ministry of Statistics and Programme Implementation (MoSPI)**.

The platform aims to identify competency gaps among professionals in India's Official Statistical System and provide personalized learning recommendations, AI-powered assessments, and continuous competency development.

## Problem Statement

**Problem Statement ID:** 26101

**Title:** Develop an AI-enabled learning platform that identifies competency gaps, recommends personalized training through integration with the iGOT Karmayogi ecosystem, and generates quizzes and multiple-choice questions (MCQs) from uploaded learning materials.

The platform addresses the challenge of helping government officials identify the skills they need to develop and providing personalized learning pathways aligned with their job roles, existing competencies, and future requirements.

## Key Features

### AI-Based Competency Assessment

* Builds competency profiles based on learner information.
* Evaluates existing skills against predefined competency frameworks.
* Supports statistical, technical, digital governance, behavioural, and managerial competencies.

### Skill-Gap Analysis

* Identifies gaps between current and required competency levels.
* Categorizes skills based on proficiency and learning priority.
* Provides actionable insights for professional development.

### Personalized Learning Recommendations

* Recommends learning resources based on individual skill gaps.
* Designed to support integration with the **iGOT Karmayogi** ecosystem.
* Supports recommendations for relevant NSSTA training programmes.
* Continuously adapts recommendations based on learner progress.

### AI-Powered Quiz & MCQ Generation

* Generates quizzes and objective-type questions from uploaded learning materials.
* Supports learning content such as documents and presentations.
* Provides automated evaluation and explanations.
* Enables continuous self-assessment and learning reinforcement.

### Learning Analytics

* Tracks learner progress and competency development.
* Provides personalized learning insights.
* Enables administrators to monitor workforce competency and training effectiveness.

## Proposed AI Architecture

```text
                    Learner Profile
                          │
                          ▼
                ┌────────────────────┐
                │ Competency Engine  │
                └─────────┬──────────┘
                          │
                          ▼
                   Skill Gap Analysis
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
    Recommendation Engine       Assessment Engine
             │                         │
             ▼                         ▼
      iGOT / NSSTA Courses       RAG + LLM Pipeline
                                       │
                                       ▼
                                  MCQs / Quizzes
                                       │
                                       ▼
                              Learner Performance
                                       │
                                       ▼
                              Updated Competency
```

## Technology Stack

### Frontend

* React
* Vite
* JavaScript
* HTML
* CSS

### AI / Machine Learning

* Python
* Large Language Models (LLMs)
* Natural Language Processing (NLP)
* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Embeddings
* Vector Database

### Backend

* Python 3.11–3.14
* FastAPI (REST API, OpenAPI/Swagger docs)
* Uvicorn (ASGI server)
* SQLAlchemy ORM
* SQLite (default; swap `DATABASE_URL` for PostgreSQL)
* Pydantic v2 (request/response validation)
* ChromaDB (persistent vector store)
* PyMuPDF / python-docx / python-pptx (document extraction)
* pytest (test suite)

The AI engines and the application API are a single FastAPI service in
`ai-backend/`, consumed by the React frontend through
`frontend/src/services/*.js`.

### Future Integrations

* iGOT Karmayogi APIs
* NSSTA training programme data
* Government digital ecosystems
* Authentication and role-based access control

## Competency Domains

The platform is designed around multiple competency areas:

**Statistical Competencies**

* Survey Design
* Sampling
* National Accounts
* Price Statistics
* Labour Statistics
* Agricultural Statistics
* Industrial Statistics
* SDG Indicators
* Metadata Standards
* Data Quality

**Technical Competencies**

* Python
* R
* SQL
* Stata
* SPSS
* SAS
* GIS
* Data Visualization
* AI/ML
* Cloud Computing
* APIs
* Open Data

**Digital Governance**

* Cybersecurity
* Data Privacy
* Digital Signatures
* Government Cloud
* Digital Public Infrastructure

**Behavioural & Managerial**

* Leadership
* Communication
* Project Management
* Ethics
* Decision Making
* Change Management

## Project Structure

```text
AI-enabled-learning-platform/
│
├── frontend/          # React + Vite web application
│   └── src/services/  # HTTP layer that talks to the backend
│
├── ai-backend/        # FastAPI backend (API + AI engines + RAG)
│   ├── app/
│   │   ├── api/           # HTTP routes
│   │   ├── services/      # competency, skill-gap, recommendation,
│   │   │                  # assessment, adaptive-learning, assistant engines
│   │   ├── ai/            # LLM provider, embeddings, RAG, MCQ generator
│   │   ├── integrations/  # iGOT Karmayogi / NSSTA providers
│   │   ├── processors/    # PDF/DOCX/PPTX/TXT extraction + chunking
│   │   ├── models/        # SQLAlchemy ORM models
│   │   ├── schemas/       # Pydantic request/response models
│   │   └── core/          # config, database, security
│   ├── tests/         # pytest suite (no API key required)
│   ├── run.py         # start the server
│   ├── seed.py        # seed demo employees/roles/competencies
│   └── smoke_test.py  # end-to-end check against a running server
│
├── HowTo.md           # Development/setup notes
│
├── LICENSE            # MIT License
│
└── README.md
```

## Getting Started

### Prerequisites

Make sure you have installed:

* Node.js and npm
* Python 3.11 or newer
* Git

### Clone the Repository

```bash
git clone https://github.com/Kash1444/AI-enabled-learning-platform.git
cd AI-enabled-learning-platform
```

### Run the Backend

The backend runs entirely offline in `DEMO_MODE` — **no API keys needed**.

```powershell
cd ai-backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python seed.py       # demo employees, roles, competencies, skill gaps
python run.py
```

The API starts on the port set by `PORT` in `ai-backend/.env`, with
interactive docs at `/docs`.

> **This checkout is configured for port 8001**, not the usual 8000,
> because 8000 was already taken on the development machine. Both
> `ai-backend/.env` (`PORT=8001`) and `frontend/.env`
> (`VITE_API_URL=http://localhost:8001`) are set to match. To move back to
> 8000, change the port in **both** files together — they must agree or
> every request fails with a connection error.

Verify everything works, with the server running:

```powershell
python smoke_test.py   # exercises every endpoint the frontend calls
pytest -q              # unit/integration suite
```

### Run the Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The development server will provide a local URL, typically:

```text
http://localhost:5173
```

`frontend/.env` sets `VITE_API_URL` to the backend origin (no `/api`
suffix — `src/services/apiClient.js` adds that itself).

### Demo Logins

| Role     | Email               | Password       |
|----------|---------------------|----------------|
| Employee | employee@demo.com   | Employee@123   |
| Trainer  | trainer@demo.com    | Trainer@123    |
| Admin    | admin@demo.com      | Admin@123      |

## API Reference

Full interactive docs at `http://localhost:8000/docs` while the backend is
running. Detailed engine documentation is in
[`ai-backend/README.md`](ai-backend/README.md).

| Method | Path | Purpose |
|---|---|---|
| GET  | `/api/health` | Health check; reports `DEMO_MODE` |
| GET  | `/api/competency/{employee_id}` | Competency overview (overall %, per-domain) |
| GET  | `/api/competency/{employee_id}/gaps` | Skill-gap analysis with priorities |
| POST | `/api/competency/assess` | Score assessment answers deterministically |
| GET  | `/api/recommendations/{employee_id}` | Ranked personalized recommendations |
| GET  | `/api/recommendations/{employee_id}/igot` | iGOT Karmayogi course recommendations |
| GET  | `/api/recommendations/{employee_id}/nssta` | NSSTA TPAC programme recommendations |
| POST | `/api/materials/upload` | Upload PDF/DOCX/PPTX/TXT (multipart) |
| GET  | `/api/materials` | List uploaded materials |
| GET  | `/api/materials/{material_id}` | Material detail + extracted chunk preview |
| POST | `/api/assessment/generate` | Generate an MCQ assessment (RAG-grounded) |
| GET  | `/api/assessment/{assessment_id}` | Fetch for a learner (answer key withheld) |
| POST | `/api/assessment/evaluate` | Grade answers, update competency, suggest next level |
| POST | `/api/assistant/chat` | AI learning assistant (RAG / profile / general) |

### AI configuration

`DEMO_MODE=true` (the default) runs the entire platform — scoring, gap
analysis, recommendations, RAG, MCQ generation, assistant — with **no
external credentials and no network calls**. Competency scoring and gap
analysis are deterministic formulas, so they are identical either way.

To enable LLM-written questions and free-form assistant answers, set in
`ai-backend/.env`:

```env
DEMO_MODE=false
LLM_PROVIDER=anthropic     # or: openai
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-sonnet-5
```

Generated questions are validated before they reach a learner; anything
malformed or ungrounded falls back to the deterministic extractive
generator rather than surfacing a broken question.

## Development Roadmap

* [x] Initial frontend development
* [x] AI competency assessment
* [x] Automated skill-gap analysis
* [x] AI-powered learning recommendations
* [x] RAG-based learning content processing
* [x] AI-generated MCQs and quizzes
* [x] Automated assessment and feedback
* [x] Learner competency tracking
* [~] iGOT Karmayogi integration — provider interface + mock data; real API
  needs credentials (`IGOT_API_BASE_URL` / `IGOT_API_KEY`)
* [~] NSSTA training programme integration — same, mock data for now
* [ ] Administrator analytics
* [ ] Multilingual learning support
* [ ] Secure authentication and role-based access control
* [ ] Cloud deployment

### Frontend wiring status

The backend implements, serves and verifies every feature above. The
frontend is **not yet wired to it** — as the app currently stands it makes
no HTTP calls to the backend at all. Closing that gap is the next task, and
none of it requires backend changes.

`src/services/` is a complete, working HTTP layer for every endpoint. What
is missing is the wiring:

1. **Two pages already call the services but are unreachable.**
   `pages/employee/AIAssistant.jsx` (`POST /api/assistant/chat`) and
   `pages/trainer/GenerateAssessment.jsx` (`POST /api/assessment/generate`)
   are never imported by `routes/AppRoutes.jsx`, so the bundler drops them.
   They need routes before they do anything.

2. **The sidebar links to routes that don't exist.**
   `components/layout/Sidebar.jsx` links to `/employee/quizzes`,
   `/employee/results` and `/employee/ai-assistant`. `AppRoutes.jsx`
   defines none of them, so the `*` catch-all sends the user back to the
   login page.

3. **`GenerateAssessment.jsx` imports `./GenerateAssessment.css`, which
   does not exist.** The build only survives because nothing imports the
   page. Adding a route for it fails the build until that file is created.

4. **`services/authService.js` imports `./api.js`, which does not exist.**
   Harmless today (nothing imports it); it breaks the build the moment
   something does. Login is currently hardcoded in `pages/Login.jsx`
   against `localStorage` — there is no backend auth endpoint.

5. **The remaining pages render static fixtures** from `src/data/` instead
   of calling the services — the employee dashboard, competencies, skill
   gaps, learning path, iGOT and NSSTA pages. Switching one over is a
   two-line change; the header comment in
   `src/services/competencyService.js` shows the exact before/after.

6. **Many files are still empty**, including every admin page, all chart
   components, and most shared/common components.

## Vision

The goal of this project is to create an intelligent, adaptive learning ecosystem that helps build a **future-ready and digitally skilled workforce for India's Official Statistical System**.

Instead of providing the same training to every learner, the platform aims to understand **what each learner already knows, identify what they need to learn, recommend the right training, assess their progress, and continuously adapt their learning journey.**

## Hackathon

**Smart India Hackathon 2026**

**Organization:** Ministry of Statistics and Programme Implementation (MoSPI)

**Department:** Data Informatics & Innovation Division (DIID)

**Category:** Software

**Theme:** Smart Education

**Problem Statement:** 26101

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
