# Story 3.5: Escalation to Human Contact

**As a** user,
**I want** to be directed to a human contact when the chatbot cannot answer my question,
**So that** I have a clear path to get the help I need.

**Covers:** FR-007

## Acceptance Criteria

1.  **Given** the chatbot has failed to answer my query after a reasonable number of attempts (or confidence is low),
    **When** it cannot find a relevant answer,
    **Then** it provides a clear and direct link to the university's contact page.

## Technical Notes

*   **Frontend:** UI component to display the contact link.
*   **Backend:** Logic in FastAPI (or Gemini prompt) to detect when to escalate (e.g., "I don't know" response or low similarity score).
