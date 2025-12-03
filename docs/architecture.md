# Architecture

## Executive Summary

This document outlines the architectural decisions for the ibe160 AI-powered chatbot. The core architecture is a full-stack Next.js frontend and FastAPI backend, deployed on Vercel, leveraging Supabase with pgvector for data persistence and Google Gemini 2.5 Pro for conversational AI. Key decisions prioritize consistency, scalability, and ease of development for an MVP, with considerations for future growth and robust handling of errors and data.

## Project Initialization

The first implementation story should execute:
```bash
npx create-next-app@latest ibe160-chatbot --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
cd ibe160-chatbot
npx shadcn-ui@latest init
```

This establishes the base architecture with these decisions:
- **Framework:** Next.js
- **Language:** TypeScript
- **Styling solution:** Tailwind CSS (with Shadcn UI for components)
- **Testing framework:** To be decided (will be covered by the testing strategy below)
- **Linting/Formatting:** ESLint (provided)
- **Build tooling:** Next.js (provided)
- **Project structure:** Next.js App Router (provided)

## Decision Summary

| Category | Decision | Version | Rationale |
| -------- | -------- | --- | --------- |
| **Core Tech** | | |
| Frontend Framework | Next.js | 16.0.6 | Modern React framework, strong for web apps. |
| Frontend UI/Styling | Tailwind CSS, Shadcn UI | | Utility-first CSS, customizable component library. |
| Backend Framework | FastAPI | 0.121.1 | High performance, easy to use, Python ecosystem. |
| Database | Supabase (PostgreSQL) | | Managed PostgreSQL, includes `pgvector` for AI. |
| Vector Database | Supabase `pgvector` | | Integrated vector search for RAG. |
| AI Model | Google Gemini 2.5 Pro | | Specified in PRD for conversational AI. |
| Deployment | Vercel (Next.js + FastAPI) | | Unified platform, simplifies deployment, serverless functions. |
| **Architectural Decisions** | | |
| API Pattern | REST | | Standard, reliable, simple to implement for Next.js/FastAPI. |
| Prompt Management | Simple Config Files (YAML) | | Flexible for iteration without database complexity, easily migrated later. |
| Token Optimization | Retrieval with Context Window Management | | Best for RAG systems, ensures relevance and efficiency, avoids token limit issues. |
| Fallback Strategy | Tiered (Rephrasing -> Human Escalation) | | Provides better UX, attempts self-resolution, then clear path to human assistance. |
| Background Jobs | Scheduled Serverless Function (Vercel Cron Jobs) | | Simplest, most integrated solution for daily scraping. |
| Email Service | Resend | | Modern, developer-friendly, integrates well with Vercel/Next.js. |
| **Cross-Cutting Concerns** | | |
| Error Handling | Standardized Responses & Centralized Logging | | Clear user feedback, robust debugging/monitoring. |
| Logging Approach | Structured Logging (JSON) & Third-Party Service | | Organized, searchable logs, powerful analysis tools (free tiers available). |
| Date/Time Handling | UTC Backend; Local Frontend Display | | Industry standard, eliminates timezone confusion, robust. |
| API Response Format | Standardized Wrapper (`{status: ..., data/error: ...}`) | | Consistency, simplifies frontend data handling, robust. |
| Testing Strategy | Unit, Integration, E2E Tests | | Comprehensive coverage at all levels, high confidence. |

## Project Structure

```
/ibe160-chatbot
├── apps/
│   ├── web/              # Next.js Frontend
│   │   ├── app/
│   │   ├── components/
│   │   ├── lib/
│   │   ├── styles/
│   │   ├── public/
│   │   └── tests/
│   │
│   ├── api/              # FastAPI Backend
│   │   ├── app/
│   │   ├── core/
│   │   ├── prompts/
│   │   ├── services/
│   │   ├── jobs/
│   │   └── tests/
│   │
├── docs/                 # Project documentation
├── .github/              # CI/CD workflows
├── .vscode/              # Editor configurations
├── .env                  # Environment variables
├── package.json          # Monorepo management/scripts
└── README.md
```

## Epic to Architecture Mapping



*   **Epic 1: Foundation & Core Chat:**

    *   **Architecture Support:** Core project setup (monorepo), basic Next.js UI (`apps/web`), basic FastAPI endpoint (`apps/api`).

*   **Epic 2: Knowledge Base & Retrieval:**

    *   **Architecture Support:** Supabase/pgvector integration (`apps/api`), web scraper (`apps/api/jobs`), RAG pipeline implementation (`apps/api/services`).

*   **Epic 3: Conversational Intelligence & User Experience:**

    *   **Architecture Support:** Interactive UI (`apps/web`), AI prompt management (`apps/api/prompts`), information synthesis logic (`apps/api/services`), tiered fallback strategy.

*   **Epic 4: Deployment & Integration:**

    *   **Architecture Support:** Vercel deployment for both frontend and backend, CI/CD (`.github/`), Vercel Cron Jobs for scheduling.



## Technology Stack Details



### Core Technologies



*   **Runtime:** Node.js (~24.0.0 LTS), Python (3.14.1)

*   **Frontend:** Next.js (16.0.6), React, TypeScript, Tailwind CSS, Shadcn UI

*   **Backend:** FastAPI (0.121.1), Python (3.14.1), SQLAlchemy (2.0.44), Supabase (`pgvector`)

*   **AI:** Google Gemini 2.5 Pro API

*   **Database Client (JS):** @supabase/supabase-js (2.86.0)

*   **Database Client (Python):** supabase-py (2.24.0)

*   **Deployment:** Vercel

*   **Email:** Resend

*   **Logging:** Structured JSON logging to a Third-Party Service



### Version Verification Log (Checked on 2025-12-03)



| Technology | Recommended Version | Status |

| --- | --- | --- |

| Node.js | ~24.0.0 (LTS) | Verified |

| Python | 3.14.1 | Verified |

| Next.js | 16.0.6 | Verified |

| FastAPI | 0.121.1 | Verified |

| SQLAlchemy | 2.0.44 | Verified |

| @supabase/supabase-js | 2.86.0 | Verified |

| supabase-py | 2.24.0 | Verified |



### Integration Points



*   **Frontend (Next.js) <-> Backend (FastAPI):** REST API over HTTPS.

*   **Backend (FastAPI) <-> AI Model (Gemini):** HTTPS API calls.

*   **Backend (FastAPI) <-> Database (Supabase):** SQLAlchemy ORM / Supabase Python client.

*   **Backend (FastAPI) <-> Vercel Cron Jobs:** Vercel's internal event triggers for serverless functions.

*   **Backend (FastAPI) <-> Logging Service:** API calls to send structured JSON logs.

*   **Backend (FastAPI) <-> Email Service (Resend):** HTTPS API calls.



## Novel Pattern Designs



The project leverages a best-in-class implementation of the "Synthesizing Conversational UI" pattern combined with a robust RAG (Retrieval Augmented Generation) pipeline. While the underlying techniques (interactive guidance, information synthesis) are innovative for university information retrieval, they are achieved through established architectural patterns rather than inventing entirely new technical patterns.



## Implementation Patterns



These patterns ensure consistent implementation across all AI agents:



### Naming Conventions



*   **API Endpoints:** Plural nouns, kebab-case for multi-word paths (e.g., `/study-programs`).

*   **Database:** Tables in `snake_case_plural` (e.g., `study_programs`), columns in `snake_case` (e.g., `program_name`).

*   **Frontend (React):** Components and their files in `PascalCase` (e.g., `ChatWindow.tsx`). Other utility files in `kebab-case` (e.g., `api-client.ts`).



### Code Organization



*   **Test Files:** Co-located with the code they test (e.g., `component.tsx` and `component.test.tsx` in the same folder).

*   **Frontend Components (`apps/web`):** Organized by type (e.g., `components/ui/`, `components/layout/`, `components/modules/`).

*   **Backend (`apps/api`):** Organized by function/domain (e.g., `routers/`, `services/`, `models/`).

*   **Shared Utilities:** `lib/` in frontend, `core/utils.py` or `utils/` in backend.



### Format Patterns



*   **API Response Wrapper:**

    *   Success: `{ "status": "success", "data": { ... } }`

    *   Error: `{ "status": "error", "error": { "code": "...", "message": "..." } }`

*   **Date/Time in JSON:** ISO 8601 strings (e.g., `2025-12-03T10:00:00Z`).



### Communication Patterns



*   **Events:** If used, `kebab-case` for event names (e.g., `user-message-sent`).

*   **Frontend State Management:** Primarily React's `useState` and `useContext` hooks.



### Lifecycle Patterns



*   **Loading States:** Consistent UI like a "typing..." indicator or subtle spinner.

*   **Error Recovery:** User actions like "Try Again" button or "Contact Support" link.

*   **Retries:** Automatic with exponential backoff for transient external API failures.



### Location Patterns



*   **API Routes (`apps/api`):** Grouped using FastAPI's `APIRouter` within `routers/` directory.

*   **Static Assets (`apps/web`):** Dedicated Next.js `public/` directory.

*   **Config Files:** Environment variables (`.env`, Vercel secrets); AI prompts in `apps/api/prompts/`.



## Consistency Rules



### Date Formatting in UI



*   Unified formatting via a single library (e.g., `date-fns`), locale-aware.



### User-Facing Errors



*   Consistent, non-intrusive UI elements (toast, alert) using standardized API error codes/messages.



## Data Architecture



*   **Database:** PostgreSQL (via Supabase)

*   **Schema:** Defined using SQLAlchemy ORM (FastAPI backend).

*   **Vector Data:** `pgvector` extension for embeddings, integrated with Supabase.



## API Contracts



*   **Design:** RESTful API using FastAPI.

*   **Specification:** Documented (e.g., with OpenAPI/Swagger, automatically generated by FastAPI).

*   **Request/Response:** Follows standardized wrapper and ISO 8601 date formats.



## Security Architecture



*   **User Authentication:** Not required for MVP (publicly accessible).

*   **Data Protection:** Secure handling of API keys (environment variables), HTTPS for all communication. Supabase provides row-level security for database access.



## Performance Considerations



*   **API Responses:** Fast, standardized responses.

*   **AI Calls:** Token optimization and efficient retrieval to minimize latency.

*   **Frontend:** Next.js optimizations (SSR/SSG/ISR), image optimization, code splitting.

*   **Database:** Optimized queries leveraging `pgvector` indexing.



## Deployment Architecture



*   **Frontend & Backend:** Vercel, leveraging Next.js's capabilities and FastAPI as serverless functions.

*   **Scheduled Tasks:** Vercel Cron Jobs for daily scraping.

*   **CI/CD:** Automated deployments via GitHub Actions upon code pushes.



## Development Environment



### Prerequisites



*   Node.js (LTS), npm/yarn/pnpm

*   Python (3.9+), Poetry (or pip/venv)

*   Git

*   Vercel CLI (optional, for local deployments)



### Setup Commands



```bash

# Clone the repository

git clone [your-repo-url]

cd ibe160-chatbot



# Initialize Next.js frontend (if not already done by starter)

# npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"

# npm install / yarn install / pnpm install



# Initialize FastAPI backend (if not already done)

# cd apps/api

# poetry install # or pip install -r requirements.txt

# poetry shell



# Install Shadcn UI (frontend)

# cd apps/web

# npx shadcn-ui@latest init



# Set up environment variables

# Create .env files in apps/web and apps/api as needed, e.g.,

# NEXT_PUBLIC_GEMINI_API_KEY=your_key

# DATABASE_URL=your_supabase_url



# Run locally

# cd apps/web && npm run dev

# cd apps/api && poetry run uvicorn main:app --reload



# Other setup as per specific project needs

```



## Architecture Decision Records (ADRs)



Key architectural decisions are documented within this architectural specification, providing rationale and context for future development.



---



_Generated by BMAD Decision Architecture Workflow v1.0_

_Date: Wednesday, December 3, 2025_

_For: BIP_