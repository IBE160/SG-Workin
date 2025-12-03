# Epic Technical Specification: Foundation & Core Chat

Date: Wednesday, December 3, 2025
Author: BIP
Epic ID: epic-1
Status: Draft

---

## Overview

This Technical Specification details Epic 1: "Foundation & Core Chat" for the ibe160 AI-powered chatbot project. This epic is foundational, establishing the core project infrastructure and delivering the most basic, end-to-end chat functionality. It directly supports the project's primary goal of providing a single, intelligent source of truth for university study program information, as outlined in the Product Requirements Document (PRD).

## Objectives and Scope

The primary objective of Epic 1 is to create a robust and scalable technical foundation for the chatbot and to implement a minimal, functional chat interface capable of receiving user input and providing a basic response. This includes setting up the development environment, configuring essential frameworks and libraries, establishing basic API communication, and preparing for future deployments.

**In-Scope:**
- Project setup with Next.js (frontend), FastAPI (backend), and Supabase (database).
- Implementation of a basic chat UI with input field and send button.
- Development of a simple API endpoint returning a hardcoded "Hello World" response.
- Setup of a basic CI/CD pipeline for automated deployment.
- Core infrastructure for future scalability.

**Out-of-Scope:**
- Advanced conversational AI logic (e.g., RAG, interactive guidance).
- Dynamic information retrieval from university websites.
- User authentication or complex data storage beyond basic Supabase setup.
- Comprehensive deployment strategies or environment management.
- Detailed error handling and logging beyond initial setup.

## System Architecture Alignment

Epic 1 directly aligns with the foundational elements of the approved architecture. The project structure (monorepo with `apps/web` for Next.js frontend and `apps/api` for FastAPI backend) is established here. The initial setup incorporates key technological decisions such as TypeScript, Tailwind CSS with Shadcn UI for the frontend, and Python/FastAPI for the backend. Supabase (PostgreSQL with `pgvector` enabled) is provisioned for future data persistence needs. Basic deployment to Vercel is also initiated, creating the pathway for the specified CI/CD strategy. This epic forms the bedrock upon which subsequent architectural components for RAG, conversational intelligence, and advanced deployment will be built.

## Detailed Design

### Services and Modules

**Frontend (`apps/web` - Next.js/React/TypeScript):**
- **ChatWindow Component:** Displays messages and provides input field and send button.
- **API Client Module:** Handles communication with the FastAPI backend.

**Backend (`apps/api` - FastAPI/Python):**
- **Main Application Module:** Entry point for the FastAPI application.
- **Chat Endpoint:** A simple API route to receive messages and return responses.

**Database (Supabase/PostgreSQL):**
- No specific data models for core chat functionality in this epic, but Supabase instance is initialized.

### Data Models and Contracts

For this epic, no complex data models are introduced.
- **Frontend Input:** Simple string representing user's message.
- **Backend Response:** Simple string representing the chatbot's hardcoded reply.
- Supabase will be initialized, but specific tables for chat history or embeddings are not part of Epic 1.

### APIs and Interfaces

**Backend API (`apps/api`):**
- **Endpoint:** `POST /chat`
  - **Description:** Receives a user message and returns a hardcoded response.
  - **Request Body:** `{ "message": "string" }`
  - **Response Body (Success):** `{ "status": "success", "data": { "reply": "string" } }`
  - **Response Body (Error):** `{ "status": "error", "error": { "code": "...", "message": "..." } }`
  - **Error Codes:** (To be defined later, basic error handling for server issues only)

**Frontend API Client (`apps/web`):**
- **`sendMessage(message: string): Promise<{ reply: string }>`:** Function to call the `POST /chat` endpoint.

### Workflows and Sequencing

1.  **Project Initialization (Story 1.1):**
    *   Developer executes setup scripts.
    *   Creates Next.js project with TypeScript, Tailwind CSS, Shadcn UI.
    *   Creates FastAPI project with SQLAlchemy.
    *   Initializes Supabase project with `pgvector` extension.
    *   Initializes Git repository.

2.  **Basic Chat Interface (Story 1.2):**
    *   User opens application in browser.
    *   Next.js renders `ChatWindow` component.
    *   User sees text input field and "Send" button.

3.  **"Hello World" Chat Response (Story 1.3):**
    *   User types message into input and clicks "Send".
    *   Frontend API client sends `POST /chat` request to FastAPI backend.
    *   FastAPI endpoint receives request and returns hardcoded "Hello!" message.
    *   Frontend displays the hardcoded response in the chat window.

4.  **Basic Deployment Pipeline (Story 1.4):**
    *   Developer pushes new commit to main branch.
    *   GitHub Actions workflow (configured via Vercel) triggers.
    *   Application is automatically deployed to Vercel.
    *   Deployed application is accessible via public URL.

## Non-Functional Requirements

### Performance

For Epic 1, the primary performance objective is rapid responsiveness for basic chat interactions and swift deployment times. The PRD specifies "near-instantaneous response to user queries" (P95 under 2 seconds). While this epic establishes the core, it will not fully implement complex RAG. Therefore, the focus is on efficient frontend rendering and low-latency API communication for hardcoded responses. Deployment time for CI/CD should be minimal.

### Security

Security in Epic 1 focuses on foundational best practices:
- **Authentication/Authorization:** Not applicable for MVP (publicly accessible).
- **API Key Handling:** Secure management of any API keys (e.g., Vercel, Supabase initial setup) via environment variables.
- **HTTPS:** All communication between frontend and backend will use HTTPS, enabled by Vercel deployment.
- **Supabase:** Initial setup will leverage Supabase's inherent security for database access, though no sensitive data handling is within this epic's scope.

### Reliability/Availability

Epic 1 lays the groundwork for a reliable system. The Vercel deployment targets high availability for the frontend and backend services. Minimal downtime during deployments is expected due to Vercel's platform features. Basic error handling for the API endpoint will be in place to prevent crashes, ensuring the system remains operational for the "Hello World" functionality.

### Observability

For Epic 1, observability efforts will be minimal but foundational:
- **Logging:** Basic structured logging for FastAPI (backend) to confirm API calls and responses.
- **Deployment Status:** Monitoring deployment success/failure via Vercel's dashboard.
- **Basic Health Checks:** Implicitly covered by successful deployment and frontend accessibility. No dedicated monitoring tools are integrated within this epic.

## Dependencies and Integrations

Epic 1 is primarily concerned with establishing the core dependencies for the project. The listed items are the foundational technologies that will be integrated. Actual dependency manifest files (e.g., `package.json`, `pyproject.toml`) will be created and managed as part of Story 1.1.

**Core Technologies:**
- **Node.js (LTS):** Runtime for Next.js frontend.
- **Python (3.14.1):** Runtime for FastAPI backend.
- **Next.js (16.0.6):** Frontend framework.
- **React:** Underlying UI library for Next.js.
- **TypeScript:** Language for frontend development.
- **Tailwind CSS:** Utility-first CSS framework for styling.
- **Shadcn UI:** Component library based on Tailwind CSS for UI components.
- **FastAPI (0.121.1):** Backend web framework.
- **SQLAlchemy (2.0.44):** Python ORM (though minimal usage in Epic 1).
- **Supabase (PostgreSQL with `pgvector`):** Database and vector store (initialization only).
- **Vercel:** Deployment platform for both frontend and backend.
- **GitHub Actions:** CI/CD integration for automated deployment.

**Integration Points (established in Epic 1):**
- **Frontend (Next.js) <-> Backend (FastAPI):** Initial REST API communication over HTTPS for the "Hello World" response.
- **GitHub <-> Vercel:** Basic CI/CD integration for automated deployments.

## Acceptance Criteria (Authoritative)

The following acceptance criteria are derived directly from the Epic 1 stories, reflecting the foundational nature of this epic.

1.  **Project Setup & Infrastructure Initialization (Story 1.1 AC):**
    *   **Given** a new project, **When** the setup script is run, **Then** a new Next.js project is created with TypeScript, Tailwind CSS, and Shadcn UI.
    *   **And** a new FastAPI project is created with SQLAlchemy.
    *   **And** a new Supabase project is created with the `pgvector` extension enabled.
    *   **And** the project is initialized as a Git repository with a main branch.
2.  **Basic Chat Interface (Story 1.2 AC):**
    *   **Given** the application is running, **When** I open the application in a browser, **Then** I see a chat window with a text input field and a "Send" button.
    *   **And** I can type a message into the input field.
3.  **"Hello World" Chat Response (Story 1.3 AC):**
    *   **Given** I have sent a message to the chatbot, **When** the chatbot receives the message, **Then** the chatbot responds with a hardcoded message (e.g., "Hello! I am the university chatbot. How can I help you today?").
4.  **Basic Deployment Pipeline (Story 1.4 AC):**
    *   **Given** a new commit is pushed to the main branch, **When** the deployment pipeline is triggered, **Then** the application is automatically deployed to a hosting provider (e.g., Vercel).
    *   **And** the deployed application is accessible via a public URL.

## Traceability Mapping

| Acceptance Criteria | Spec Section (PRD/Epic) | Component(s)/API(s) | Test Idea |
| :------------------ | :---------------------- | :------------------ | :-------- |
| 1.1.1 Next.js project created | Epic 1, Story 1.1 | `npx create-next-app` | Verify project files |
| 1.1.2 FastAPI project created | Epic 1, Story 1.1 | `poetry new` | Verify project files |
| 1.1.3 Supabase init | Epic 1, Story 1.1 | `supabase init` | Verify Supabase setup |
| 1.1.4 Git init | Epic 1, Story 1.1 | `git init` | Verify .git folder |
| 1.2.1 Chat UI displayed | Epic 1, Story 1.2, FR-003 | `apps/web/ChatWindow.tsx` | UI component test |
| 1.2.2 User can type | Epic 1, Story 1.2, FR-003 | `apps/web/ChatWindow.tsx` | UI interaction test |
| 1.3.1 Chatbot responds | Epic 1, Story 1.3, FR-003 | `apps/api/chat` (POST) | API integration test |
| 1.3.2 Hardcoded message | Epic 1, Story 1.3, FR-003 | `apps/api/chat` (POST) | API integration test |
| 1.4.1 Auto-deploy on commit | Epic 1, Story 1.4, FR-001 | `.github/workflows` (CI/CD) | End-to-end deployment test |
| 1.4.2 Public access | Epic 1, Story 1.4, FR-001 | Vercel Deployment | Manual/Automated URL check |

## Risks, Assumptions, Open Questions

**Risks:**
-   **Integration Complexity:** Integrating Next.js, FastAPI, and Supabase might present initial configuration challenges, potentially delaying the foundational setup. (Impact: High, Likelihood: Medium)
-   **Deployment Configuration:** Setting up Vercel for a monorepo with both Next.js and FastAPI could have a learning curve. (Impact: Medium, Likelihood: Medium)
-   **Tooling/Dependency Conflicts:** Potential conflicts between Python and Node.js environments or dependencies if not carefully managed. (Impact: Low, Likelihood: Medium)

**Assumptions:**
-   **Tool Availability:** Necessary tools (Node.js, Python, Git, Vercel CLI) are installed and configured in the development environment.
-   **Vercel Account:** A Vercel account capable of deploying both Next.js and FastAPI (via Serverless Functions) is available.
-   **Supabase Access:** Access to a Supabase project and the ability to enable extensions.

**Open Questions:**
-   What specific testing framework will be chosen for frontend and backend unit/integration tests? (To be decided in later epics or during sprint planning).
-   Are there specific naming conventions beyond those outlined in the Architecture document that need to be enforced during initial setup?

## Test Strategy Summary

For Epic 1, the test strategy focuses on verifying foundational setup and basic functionality.

-   **Unit Tests:** (Future consideration) Basic unit tests for individual functions in the frontend (e.g., API client utility) and backend (e.g., API endpoint handler logic) to ensure correctness.
-   **Integration Tests:** Verify the successful interaction between the frontend (Next.js) and backend (FastAPI) for the "Hello World" chat response.
-   **End-to-End (E2E) Tests:** A basic E2E test to simulate a user opening the application, typing a message, clicking send, and receiving the hardcoded response.
-   **Deployment Verification:** Automated checks (via CI/CD) to confirm successful deployment to Vercel and accessibility of the public URL.
-   **Manual Verification:** Manual checks to ensure project structure is correctly initialized, dependencies are installed, and UI components render as expected.