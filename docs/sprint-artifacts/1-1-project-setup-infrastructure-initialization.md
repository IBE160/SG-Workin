# Story 1.1: Project Setup & Infrastructure Initialization

Status: drafted

## Story

As a developer,
I want to set up the project structure and core dependencies,
So that I have a foundation for building the application.

## Story Context Summary

### Epic: Foundation & Core Chat (Epic 1)

This story is part of Epic 1, which establishes the core project infrastructure and delivers the most basic, end-to-end chat functionality.

### Story 1.1: Project Setup & Infrastructure Initialization

**User Story:**
As a developer,
I want to set up the project structure and core dependencies,
So that I have a foundation for building the application.

**Acceptance Criteria:**
*   **Given** a new project, **When** the setup script is run, **Then** a new Next.js project is created with TypeScript, Tailwind CSS, and Shadcn UI.
*   **And** a new FastAPI project is created with SQLAlchemy.
*   **And** a new Supabase project is created with the `pgvector` extension enabled.
*   **And** the project is initialized as a Git repository with a main branch.

**Architectural Guidance & Constraints:**
The project initialization involves setting up a full-stack Next.js frontend and FastAPI backend deployed on Vercel, leveraging Supabase with `pgvector`.
- **Frontend Setup:** Use `npx create-next-app@latest ibe160-chatbot --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"` followed by `npx shadcn-ui@latest init`.
- **Backend Setup:** FastAPI with Python 3.14.1 and SQLAlchemy 2.0.44.
- **Database:** Supabase (PostgreSQL with `pgvector`).
- **Project Structure:** Monorepo (`apps/web` for Next.js, `apps/api` for FastAPI).
- **Naming Conventions:**
  - Frontend components: `PascalCase`
  - Utility files: `kebab-case`
  - Database tables: `snake_case_plural`
  - Database columns: `snake_case`
- **Code Organization:** Test files co-located.
- **Prerequisites:** Node.js (LTS), Python (3.9+), Poetry, Git, Vercel CLI.

## Acceptance Criteria

1. **Given** a new project, **When** the setup script is run, **Then** a new Next.js project is created with TypeScript, Tailwind CSS, and Shadcn UI. (AC #1)
2. **And** a new FastAPI project is created with SQLAlchemy. (AC #2)
3. **And** a new Supabase project is created with the `pgvector` extension enabled. (AC #3)
4. **And** the project is initialized as a Git repository with a main branch. (AC #4)

## Tasks / Subtasks

- [ ] Task 1: Initialize Next.js Frontend (AC: #1)
  - [ ] Subtask 1.1: Run `npx create-next-app@latest ibe160-chatbot --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"`
  - [ ] Subtask 1.2: Run `npx shadcn-ui@latest init` to setup Shadcn UI.
  - [ ] Subtask 1.3: Verify Next.js project structure and dependencies.
- [ ] Task 2: Initialize FastAPI Backend (AC: #2)
  - [ ] Subtask 2.1: Setup Poetry environment for Python 3.14.1.
  - [ ] Subtask 2.2: Add `fastapi`, `sqlalchemy` to `pyproject.toml`.
  - [ ] Subtask 2.3: Create basic `apps/api` directory structure.
- [ ] Task 3: Initialize Supabase (AC: #3)
  - [ ] Subtask 3.1: Create a new Supabase project.
  - [ ] Subtask 3.2: Enable `pgvector` extension in the Supabase project.
- [ ] Task 4: Initialize Git Repository (AC: #4)
  - [ ] Subtask 4.1: Run `git init`.
  - [ ] Subtask 4.2: Create an initial commit with the project structure.
- [ ] Task 5: Testing & Validation
  - [ ] Subtask 5.1: Manually verify all project initialization steps were successful.

## Dev Notes

- Relevant architecture patterns and constraints:
  - Frontend: Next.js with TypeScript, Tailwind CSS, Shadcn UI.
  - Backend: FastAPI with Python 3.14.1, SQLAlchemy 2.0.44.
  - Database: Supabase with `pgvector` extension.
  - Project Structure: Monorepo (`apps/web`, `apps/api`).
  - Deployment: Vercel.
- Source tree components to touch: Initial project setup commands will create the basic directory structure.
- Testing standards summary: Manual verification of setup.

### Project Structure Notes

- Alignment with unified project structure: The initial setup will establish the `ibe160-chatbot` monorepo structure with `apps/web` and `apps/api` as per the architectural guidelines.
- Detected conflicts or variances: None expected during initial setup.

### References

- [Source: docs/PRD.md]
- [Source: docs/architecture.md]
- [Source: .bmad/bmm/workflows/4-implementation/epic-tech-context/tech-spec-epic-epic-1.md]