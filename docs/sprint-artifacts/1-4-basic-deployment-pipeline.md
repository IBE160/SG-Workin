# Story 1.4: Basic Deployment Pipeline

Status: ready-for-dev

## Story

As a developer,
I want to set up a basic deployment pipeline,
So that I can automatically deploy the application.

## Acceptance Criteria

1. **Given** a new commit is pushed to the main branch, **When** the deployment pipeline is triggered, **Then** the application is automatically deployed to a hosting provider (e.g., Vercel).
2. **And** the deployed application is accessible via a public URL.
3. **And** both Frontend (Next.js) and Backend (FastAPI) are functional in the deployed environment.

## Tasks / Subtasks

- [ ] Task 1: Configure Vercel Project (AC: #1)
  - [ ] Subtask 1.1: Create **Two Vercel Projects** connected to the git repo:
      - Project A: "ibe160-frontend" (Root: `frontend`, Framework: Next.js)
      - Project B: "ibe160-backend" (Root: `backend`, Framework: FastAPI/Python)
  - [ ] Subtask 1.2: Generate `requirements.txt` for Vercel: Run `uv export --format requirements-txt > backend/requirements.txt` (Vercel doesn't support uv natively yet).
  - [ ] Subtask 1.3: Set up Environment Variables in Vercel:
      - Frontend: `NEXT_PUBLIC_API_URL` (Production URL of Backend)
      - Backend: `ALLOWED_ORIGINS` (Production URL of Frontend)
  - [ ] Subtask 1.4: Update `backend/main.py` to use `ALLOWED_ORIGINS` env var in `CORSMiddleware`.
- [ ] Task 2: Deployment Verification (AC: #2, #3)
  - [ ] Subtask 2.1: Add a simple GET `/health` endpoint in `backend/main.py` return `{"status": "ok"}`.
  - [ ] Subtask 2.2: Push code (including `requirements.txt`) to trigger deployment.
  - [ ] Subtask 2.2: Verify Frontend is accessible at public URL.
  - [ ] Subtask 2.3: Verify Backend API is reachable (e.g., `/api/messages`).
  - [ ] Subtask 2.4: Verify Frontend can talk to Backend (Chat "Hello" test).

## Dev Notes

- **Architecture Compliance:**
    - Deployment Target: Vercel.
    - Monorepo structure: `frontend` (Next.js) and `backend` (FastAPI).
    - **CRITICAL**: The architecture doc mentions `apps/web` and `apps/api`, but the ACTUAL structure is `frontend` and `backend`. Use the ACTUAL structure.
- **Vercel Configuration:**
    - May need `vercel.json` in root to define routes/builds.
    - Python runtime for backend.
    - Node.js runtime for frontend.
- **Environment Variables:**
    - Frontend needs `NEXT_PUBLIC_API_URL` pointing to the deployed backend URL.

### Project Structure Notes

- **ACTUAL:** `frontend/` and `backend/` directories.
- **DOCS:** `apps/web` and `apps/api` (Discrepancy noted).

### References

- [Source: docs/epics.md#Section-Story-1.4]
- [Source: docs/architecture.md#Section-Deployment-Architecture]

## Dev Agent Record

### Context Reference

### Agent Model Used

Google Gemini 2.0 Flash Experimental

### Debug Log References

### Completion Notes List

### File List
