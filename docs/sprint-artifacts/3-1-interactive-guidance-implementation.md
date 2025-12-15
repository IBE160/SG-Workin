# Story 3.1: Interactive Guidance Implementation

## Story

**As a** user,
**I want** the chatbot to ask clarifying questions when my query is ambiguous,
**So that** I can get more precise answers.

## Acceptance Criteria

1.  **Given** I ask an ambiguous question (e.g., "Tell me about business"),
2.  **When** the chatbot processes the query,
3.  **Then** it detects the ambiguity.
4.  **And** it responds with a clarifying question (e.g., "Are you interested in a specific business degree, or would you like to know about business courses in general?").
5.  **And** it does *not* attempt a RAG search yet, or performs a broad search but prioritizes clarification.
6.  **Given** I answer the clarifying question,
7.  **When** the chatbot receives the follow-up,
8.  **Then** it uses the combined context to perform a specific RAG search.

## Tasks / Subtasks

- [ ] **Task 1: Ambiguity Detection Logic**
    -   Create a method (e.g., `detect_ambiguity(query)`) in `RagService` or a new service.
    -   Use Gemini to analyze the query.
    -   Define a system prompt `AMBIGUITY_PROMPT` that instructs the LLM to classify if a query is "specific" or "ambiguous" and generation of a clarifying question if ambiguous.
    -   *Constraint*: This check should be fast. Use `Gemini 2.0 Flash` if possible, or `Pro` with low tokens.

- [ ] **Task 2: Chat API Update**
    -   Update `POST /api/chat` in `backend/routers/chat.py`.
    -   Add logic to check ambiguity before full RAG.
    -   If ambiguous, return the clarifying question immediately.
    -   Protocol: Does the frontend need a specific flag? E.g., `type: "clarification"`.
    -   *Decision*: Use standard message format but perhaps add metadata/intent field.

- [ ] **Task 3: Conversation Context Handling**
    -   Ensure the chat functionality supports follow-up answers.
    -   Current `ChatRequest` might just be single turn.
    -   Need to support `history` or `messages` list in `ChatRequest`.
    -   Update `RagService` to concatenate history for the final RAG query.

- [ ] **Task 4: Verification**
    -   Automated test: `tests/test_interactive_guidance.py`.
        -   Test with known ambiguous queries ("business", "courses").
        -   Test with specific queries ("Bachelor in Sport Management").
    -   Manual validation via Chat UI.

## Technical Specifics

### Architecture Compliance
-   **Service**: Enhance `RagService` or add `ConversationService`.
-   **LLM**: Gemini for classification (low latency is key).
-   **API**: `ChatRequest` schema update to include conversation history.

### Prompt Strategy (Draft)
```text
System: You are a helpful assistant for University of Molde. Your job is to determine if a student's query is specific enough to search for a definitive answer or if it is too broad/ambiguous.

Query: "{query}"

If the query is specific (e.g., "What are the admission requirements for Nursing?", "Who is the dean of Logistics?"), output: {"status": "specific"}

If the query is ambiguous (e.g., "Tell me about studies", "business", "nursing"), output: {"status": "ambiguous", "clarifying_question": "..."}
```

## References
-   **Epic**: Epic 3, Story 3.1
-   **PRD**: FR-004 Interactive Guidance

## File List
-   backend/services/rag.py (modify)
-   backend/core/config.py (add prompt)
-   backend/routers/chat.py (modify)
-   backend/schemas/chat.py (modify for history)
