# Story 1.3: "Hello World" Chat Response

Status: Ready for Review

## Story

As a user,
I want to receive a simple, hardcoded response from the chatbot,
So that I can confirm the chat functionality is working.

## Acceptance Criteria

1. **Given** I have sent a message to the chatbot, **When** the chatbot receives the message, **Then** the chatbot responds with a hardcoded message (e.g., "Hello! I am the university chatbot. How can I help you today?").

## Tasks / Subtasks

- [x] Task 1: Create Backend API Endpoint (AC: #1)
  - [x] Subtask 1.1: Create `apps/api/app/routers/chat.py` with a `POST /chat` endpoint.
  - [x] Subtask 1.2: Implement the endpoint to accept a message payload and return the hardcoded response: "Hello! I am the university chatbot. How can I help you today?".
  - [x] Subtask 1.3: Register the router in `apps/api/app/main.py`.
  - [x] Subtask 1.4: Validation - Test endpoint via Swagger UI (usually at `/docs`) or `curl`.
- [x] Task 2: Connect Frontend to Backend (AC: #1)
  - [x] Subtask 2.1: Update `ChatWindow.tsx` (or `ChatInput.tsx` depending on state ownership) to call `POST /api/chat` when "Send" is clicked.
  - [x] Subtask 2.2: Handle the response and add the bot's message to the chat history state.
  - [x] Subtask 2.3: Verify the full flow: Type "Hi" -> Click Send -> See "Hello! ..." response in UI.

## Dev Notes

- **Architecture Compliance:**
    - **Backend:** FastAPI. Use `APIRouter`.
    - **API Contract:**
        - Request: JSON `{ "message": "string" }` (Define Pydantic model if good practice, or simple dict for MVP).
        - Response: Standard Wrapper `{ "status": "success", "data": { "response": "Hello! ..." } }`.
    - **Frontend:** Use `fetch` or a utility wrapping fetch to hit the backend. Ensure CORS is configured if running on different ports (Next.js rewrites may be needed or FastAPI CORS middleware).
- **UX Requirements:**
    - Bot message should appear in the "Bot bubble" styling (Left aligned, Neutral background).
- **Source tree components to touch:**
    - `apps/api/app/routers/chat.py` (New)
    - `apps/api/app/main.py`
    - `apps/web/components/modules/chat/ChatWindow.tsx`
- **Testing standards summary:**
    - Manual verification via UI and Swagger.

### Project Structure Notes

- **API Organization:** Routers should be in `apps/api/app/routers`.
- **Naming:** Endpoint `/chat` fits the resource.

### References

- [Source: docs/epics.md#Section-Story-1.3]
- [Source: docs/architecture.md#Section-API-Response-Wrapper]

## Dev Agent Record

### Context Reference

### Agent Model Used

Google Gemini 2.0 Flash Experimental

### Debug Log References

### Completion Notes List

- Implemented backend API and frontend integration.
- Fixed CORS/IPv6 issue by using 127.0.0.1.
- Addressed Code Review: Fixed test consistency, added docstrings, fixed git tracking.

### File List
