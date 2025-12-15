# Story 1.2: Basic Chat Interface

Status: Done

## Story

As a user,
I want to see a basic chat interface,
So that I can interact with the chatbot.

## Acceptance Criteria

1. **Given** the application is running, **When** I open the application in a browser, **Then** I see a chat window with a text input field and a "Send" button.
2. **And** I can type a message into the input field.

## Tasks / Subtasks

- [x] Task 1: Create Chat Interface Layout (AC: #1)
  - [x] Subtask 1.1: Create `apps/web/app/page.tsx` (or similar main entry) with a basic layout structure.
  - [x] Subtask 1.2: Implement `ChatWindow` component in `apps/web/components/modules/chat/ChatWindow.tsx` (Use 'sharp & modern' styling per UX).
  - [x] Subtask 1.3: Implement `ChatInput` component in `apps/web/components/modules/chat/ChatInput.tsx` (Fixed to bottom on mobile, prominent send button with `Send` icon from `lucide-react`). ensure input has `aria-label="Chat input"` for accessibility.
- [x] Task 2: Implement Message Input Interaction (AC: #2)
  - [x] Subtask 2.1: Add state management for input text (React `useState`).
  - [x] Subtask 2.2: Verify typing updates the state.
  - [x] Subtask 2.3: Add "Send" button click handler (Implemented as API call via Story 1.3 integration).

## Dev Notes

- **Architecture Compliance:**
    - Use Next.js 16.0.6 App Router.
    - Use Tailwind CSS and Shadcn UI components (install if needed via `npx shadcn-ui@latest add button input`).
    - Components should be in `apps/web/components`.
    - Naming: `PascalCase` for components.
    - Icons: Use `lucide-react` (e.g., `Send` icon).
- **UX Requirements:**
    - "Sharp & Modern" aesthetic.
    - Typography: Ensure `Inter` (or default sans) font variable is applied to layout.
    - Chat Bubble: User bubbles right-aligned (Primary Color `#2A4B7C`), Bot bubbles left-aligned (Neutral `#F5F5F5` with outline).
    - Input Area: Always visible, fixed to bottom.
- **Source tree components to touch:**
    - `apps/web/app/page.tsx`
    - `apps/web/components/modules/chat/`
- **Testing standards summary:**
    - Add basic render test for `ChatWindow` (verify input and button appear).

### Project Structure Notes

- Alignment with unified project structure: `apps/web` is the frontend root.
- Detected conflicts or variances: None.

### References

- [Source: docs/epics.md#Section-Story-1.2]
- [Source: docs/architecture.md#Section-Frontend-Components]
- [Source: docs/ux-design-specification.md#Section-Component-Library]

## Dev Agent Record

### Context Reference

### Agent Model Used

Google Gemini 2.0 Flash Experimental

### Debug Log References

### Completion Notes List

- Implemented chat layout and components.
- Added interaction logic (state, send button).
- Added unit tests for layout and interaction.
- Verified all acceptance criteria.
- Refactored `ChatInput` to use Shadcn UI components (Code Review finding).

### File List

- frontend/app/page.tsx
- frontend/components/modules/chat/ChatWindow.tsx
- frontend/components/modules/chat/ChatInput.tsx
- frontend/__tests__/chat.test.tsx
- frontend/package.json
- frontend/components/ui/button.tsx
- frontend/components/ui/input.tsx
