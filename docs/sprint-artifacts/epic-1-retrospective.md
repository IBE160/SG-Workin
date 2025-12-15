# Retrospective: Epic 1 - Foundation & Core Chat

- **Date:** 2025-12-10
- **Facilitator:** Bob (Scrum Master)
- **Participants:** Alice (PO), Charlie (Senior Dev), Dana (QA), Elena (Junior Dev), orjan (Project Lead)
- **Epic Status:** Completed (100%)

## 1. Executive Summary

Epic 1 was a success, delivering 100% of planned stories (4/4) and resulting in a live, deployed application on Vercel. The team successfully established the frontend (Next.js), backend (FastAPI), and database (Supabase) foundation. Key friction points were related to documentation/structure alignment and manual deployment configurations.

## 2. Delivery Metrics

| Metric | Value | Notes |
| :--- | :--- | :--- |
| **Stories Completed** | 4 / 4 | 100% Completion |
| **Velocity** | - | First epic, baseline established |
| **Blockers Resolved** | 1 | Environment Variable configuration for Vercel |
| **Production Status** | Live | Frontend & Backend accessible publicy |

## 3. What Went Well (Successes)

*   **Speed to Visuals:** The Basic Chat Interface (Story 1.2) was implemented quickly, providing immediate visual feedback and stakeholder value.
*   **Deployment Architecture:** The separation of concerns between `frontend` and `backend` on Vercel is working well, despite initial setup complexity.
*   **Tooling:** The team effectively used `uv` for Python dependency management, simplifying the backend setup.
*   **Testing:** Basic "Hello World" endpoint validation (Story 1.3) was straightforward and proved the integration works.

## 4. Challenges & Learnings

*   **Documentation vs. Reality:** There was confusion caused by `docs/architecture.md` referencing `apps/web` while the actual project uses `frontend/`.
    *   *Learning:* Architecture docs must be kept in sync with the scaffolded reality immediately.
*   **Artifact Standardization:** Story 1.1's artifacts were stored in `.bmad-ephemeral/stories` while others were in `docs/sprint-artifacts`, making it hard to find the full history.
    *   *Learning:* All story artifacts must follow a strict location standard.
*   **Manual Ops:** Configuring environment variables in the Vercel dashboard was a manual step that slowed down the "automated" pipeline.
    *   *Learning:* We need to look into automating this or documenting it better for future environments.

## 5. Action Items

| Priority | Action Item | Owner | Status |
| :--- | :--- | :--- | :--- |
| **High** | **Update Architecture Docs:** Align `architecture.md` to reflect `frontend`/`backend` structure. | Charlie | Pending |
| **High** | **Standardize Artifacts:** Move Story 1.1 files from `.bmad` to `docs/sprint-artifacts`. | Bob | Pending |
| **Critical** | **Epic 2 Scraper Target:** Update Story 2.2 specs with target URL: `https://www.himolde.no/studier/programmer/`. | Alice | Pending |
| **Low** | **Automate Env Vars:** Research Vercel CLI/Terraform for env var management. | Charlie | Backlog |

## 6. Next Epic Readiness (Epic 2: Knowledge Base & Retrieval)

*   **Focus:** RAG Pipeline, Supabase pgvector, Web Scraper.
*   **Risk:** Python environment for scraper (Playwright/BeautifulSoup) needs verification.
*   **Prep:** URL target identified (`https://www.himolde.no/studier/programmer/`).

---
*Signed: Bob (Scrum Master)*
