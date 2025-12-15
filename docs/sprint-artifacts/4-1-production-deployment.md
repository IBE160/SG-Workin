# Story 4.1: Production Deployment

**Status**: review

## Story

**As a** developer,
**I want** to deploy the application to a production environment,
**So that** it is publicly accessible.

**Covers:** FR-001 (Production Availability)

## Acceptance Criteria

1.  **Given** the application is ready for production,
    **When** the deployment script is run,
    **Then** the application is deployed to the production environment on Vercel.
2.  **And** the production deployment is stable and accessible via a public URL.
3.  **And** the backend (FastAPI) is correctly serving API requests via Vercel Serverless Functions.
4.  **And** the database (Supabase) is connected and accessible from the production environment.

## Tasks / Subtasks

- [ ] **Technical Configuration**
    - [ ] Create `vercel.json` for monorepo deployment (Frontend + Backend rewrites).
    - [ ] Create `backend/api/index.py` adapter for Vercel Serverless Function entry point.
    - [ ] Verify `backend/requirements.txt` is updated and clean for production.

- [ ] **Environment Setup**
    - [ ] Identify all required Environment Variables (`SUPABASE_URL`, `SUPABASE_KEY`, `GOOGLE_API_KEY`, etc.).
    - [ ] Document specific production values (e.g., using the separate Production Supabase Instance if applicable, otherwise same instance).

- [ ] **Deployment Execution**
    - [ ] Run deployment via Vercel CLI (or connect Git repository to Vercel).
    - [ ] Verify build logs for success.

- [ ] **Verification**
    - [ ] **Load Testing**: Execute `locust -f backend/tests/load/locustfile.py` against the production URL. Target: < 2s P95 latency.
    - [ ] **Deployment Config**: Ensure `vercel.json` and `backend/api/index.py` from the Verification Spike are included in the commit.
    - [ ] **Health Check**: Verify `GET /api/health` returns status: ok.
    - [ ] **RAG Functionality**: Manual test: "What are the admission requirements?" -> Verify answer + source links.

## Implementation Notes

**Deployment Architecture:**
-   **Platform**: Vercel
-   **Strategy**: Monorepo deployment.
    -   Frontend: Next.js (standard Vercel build).
    -   Backend: Python Serverless Function. Vercel detects `api/*.py` or can be configured via `vercel.json` builds.
-   **Routing**: Requests to `/api/*` must be routed to the Python backend.

**Critical Files:**
-   `vercel.json`: Handles the routing and build definitions.
-   `backend/api/index.py`: The WSGI/ASGI entry point for Vercel.

**Environment Variables:**
-   Must be set in Vercel Project Settings.
-   Do NOT commit `.env` files.

## References
-   [Architecture: Deployment](../../architecture.md#deployment-architecture)
-   [Epic 4 Definition](../epics.md#epic-4-deployment--integration)
