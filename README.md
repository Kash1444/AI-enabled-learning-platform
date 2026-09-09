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

The AI services will be exposed through APIs and integrated with the main application backend.

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
├── frontend/          # Web application
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

* Node.js
* npm
* Git

### Clone the Repository

```bash
git clone https://github.com/Kash1444/AI-enabled-learning-platform.git
cd AI-enabled-learning-platform
```

### Run the Frontend

```bash
cd frontend
npm install
npm run dev
```

The development server will provide a local URL, typically:

```text
http://localhost:5173
```

## Development Roadmap

* [x] Initial frontend development
* [ ] AI competency assessment
* [ ] Automated skill-gap analysis
* [ ] AI-powered learning recommendations
* [ ] RAG-based learning content processing
* [ ] AI-generated MCQs and quizzes
* [ ] Automated assessment and feedback
* [ ] Learner competency tracking
* [ ] iGOT Karmayogi integration
* [ ] NSSTA training programme integration
* [ ] Administrator analytics
* [ ] Multilingual learning support
* [ ] Secure authentication and role-based access control
* [ ] Cloud deployment

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
