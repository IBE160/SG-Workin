# Story 1.3: "Hello World" Chat Response

Status: Done

## Story

As a user,
I want to receive a simple, hardcoded response from the chatbot,
So that I can confirm the chat functionality is working.

## Acceptance Criteria

1. **Given** I have sent a message to the chatbot, **When** the chatbot receives the message, **Then** the chatbot responds with a hardcoded message (e.g., "Hello! I am the university chatbot. How can I help you today?").

## Tasks / Subtasks

- [x] Task 1: Create Backend API Endpoint (AC: #1)
  - [x] Subtask 1.1: Create `apps/api/app/routers/messages.py` with a `POST /messages` endpoint.
  - [x] Subtask 1.2: Implement the endpoint to accept a message payload and return the hardcoded response: "Hello! I am the university chatbot. How can I help you today?".
  - [x] Subtask 1.3: Register the router in `apps/api/app/main.py`.
  - [x] Subtask 1.4: Implement a unit test in `apps/api/app/tests/test_messages.py` to verify the endpoint returns the correct response.
  - [x] Subtask 1.5: Validation - Verify tests pass (`pytest`) and check endpoint via Swagger UI.
- [x] Task 2: Connect Frontend to Backend (AC: #1)
  - [x] Subtask 2.1: Update `ChatWindow.tsx` (or `ChatInput.tsx`) to call `POST /messages` using the `NEXT_PUBLIC_API_URL` environment variable.
  - [x] Subtask 2.2: Handle the response and add the bot's message to the chat history state.
  - [x] Subtask 2.3: Verify the full flow: Type "Hi" -> Click Send -> See "Hello! ..." response in UI.

## Dev Notes

- **Architecture Compliance:**
    - **Backend:** FastAPI. Use `APIRouter`.
    - **API Contract:**
        - Request: JSON `{ "message": "string" }` (Define Pydantic model if good practice, or simple dict for MVP).
        - Response: Standard Wrapper `{ "status": "success", "data": { "response": "Hello! ..." } }`.
    - **Frontend:** Use `fetch` or a utility wrapping fetch to hit the backend. Use `NEXT_PUBLIC_API_URL` to avoid hardcoding the backend URL. Ensure CORS is configured.
- **UX Requirements:**
    - Bot message should appear in the "Bot bubble" styling (Left aligned, Neutral background).
- **Source tree components to touch:**
    - `apps/api/app/routers/messages.py` (New)
    - `apps/api/app/main.py`
    - `apps/web/components/modules/chat/ChatWindow.tsx`
- **Testing standards summary:**
    - Unit tests required for new endpoint (`pytest`).
    - Manual verification via UI.

### Project Structure Notes

- **API Organization:** Routers should be in `apps/api/app/routers`.
- **Naming:** Endpoint `/messages` fits the resource (sending a message).

### References

- [Source: docs/epics.md#Section-Story-1.3]
- [Source: docs/architecture.md#Section-API-Response-Wrapper]

## Dev Agent Record

### Context Reference

### Agent Model Used

Google Gemini 2.0 Flash Experimental

### Debug Log References

### Completion Notes List

- Implemented `POST /messages` endpoint in `backend/routers/messages.py`.
- Registered router in `backend/main.py`.
- Verified with unit tests in `backend/tests/test_messages.py`.
- Updated `frontend/app/page.tsx` to use `NEXT_PUBLIC_API_URL` and call `/messages` endpoint.
- NOTE: Mapped story paths `apps/api` -> `backend` and `apps/web` -> `frontend` to match actual project structure.

### File List

- backend/routers/messages.py
- backend/tests/test_messages.py
- backend/main.py
- backend/pyproject.toml
- backend/tests/__init__.py
- backend/core/constants.py
- backend/uv.lock
- frontend/app/page.tsx
