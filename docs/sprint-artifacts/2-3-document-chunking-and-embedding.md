# Story 2.3: Document Chunking and Embedding

Status: Done

## Story

As a developer,
I want to process extracted website content by chunking it and generating embeddings using Google Gemini,
So that the content can be stored in the vector database for RAG.

## Acceptance Criteria

1.  **Given** the `ScraperService` successfully returns a list of program documents,
2.  **When** the `IngestionService` is triggered,
3.  **Then** it iterates through each document and splits the `content` into manageable chunks (e.g., ~1000 characters with overlap).
4.  **And** for each chunk, it generates a vector embedding using Google Gemini's `text-embedding-004` model (768 dimensions).
5.  **And** it guarantees idempotency by removing any existing chunks for the URL before inserting new ones (preventing duplicates).
6.  **And** it stores the chunk text, embedding, URL, and metadata in the Supabase `document_chunks` table.
7.  **And** the process handles API rate limits and network errors robustly using `tenacity` retry logic.

## Tasks / Subtasks

- [ ] Task 1: Setup & Dependencies
    - [ ] Subtask 1.1: Add `google-generativeai` to `backend/pyproject.toml` (or `requirements.txt`).
    - [ ] Subtask 1.2: Configure `GOOGLE_API_KEY` in `backend/core/config.py` (ensure `.env` has it).

- [ ] Task 2: Implement Ingestion Service (`backend/services/ingestion.py`)
    - [ ] Subtask 2.1: Create `IngestionService` class.
    - [ ] Subtask 2.2: Implement `_chunk_text(text, chunk_size=1000, overlap=200)` method.
        -   *Note*: Use a simple sliding window or sentence-aware splitter (regex). No heavy NLP lib needed yet.
    - [ ] Subtask 2.3: Implement `_generate_embeddings(texts)` method using `google.generativeai.embed_content`.
        -   *Note*: Use model `models/text-embedding-004`. Implement batching (10-20 items). Wrap call with `tenacity` retry logic to handle rate limits/transient errors.
    - [ ] Subtask 2.4: Implement `process_and_store(documents)` method.
        -   Connects to Supabase using `backend/core/config.py` credentials (SERVICE_ROLE key required for writes).
        -   **Critical**: Perform a delete operation for the `url` before insertion to ensure idempotency.
        -   Maps `ScrapedDocument` to `document_chunks` schema (`content`, `embedding`, `metadata`={source, title}, `url`).
        -   Inserts data.

- [ ] Task 3: API Integration
    - [ ] Subtask 3.1: Create `backend/routers/ingestion.py` with `POST /api/ingest`.
    - [ ] Subtask 3.2: Endpoint should trigger the full pipeline: Scrape (via `ScraperService`) -> Ingest (via `IngestionService`).
    - [ ] Subtask 3.3: Register router in `backend/main.py`.

- [ ] Task 4: Verification
    - [ ] Subtask 4.1: Run the ingestion via API.
    - [ ] Subtask 4.2: Verify data in Supabase Dashboard (rows in `document_chunks` with embeddings).

## Dev Notes

-   **Architecture Compliance**:
    -   **Dependencies**: Keep it lightweight. Use `google-generativeai` directly. Add `tenacity` for robust API calls. Avoid adding LangChain/LlamaIndex unless absolutely necessary for advanced splitting (simple regex splitting is fine for MVP).
    -   **Database**: Use `supabase-py` client (already in project) for DB interactions.
    -   **Security**: Use `SUPABASE_SERVICE_ROLE_KEY` for writing to the `document_chunks` table (as per Story 2.1 RLS).
    -   **Environment**: Ensure `GOOGLE_API_KEY` is loaded.

-   **Technical Specifics**:
    -   **Chunking Strategy**:
        -   Target size: ~1000 characters.
        -   Overlap: ~200 characters (to preserve context across boundaries).
        -   Split on: Newlines or periods to avoid breaking sentences mid-word.
    -   **Embedding Model**: `models/text-embedding-004`. Output dimension is 768.
    -   **Batching**: Gemini API `embed_content` accepts a list. Batch chunks (e.g., 10-20 at a time) to improve throughput and stay within rate limits.

-   **Previous Story Context**:
    -   **Story 2.1**: Table `document_chunks` exists.
    -   **Story 2.2**: `ScraperService` exists and returns `title`, `url`, `content` (deep scraped), `description`.
    -   **Ingestion**: Should leverage the `content` field from the scraper.

## References

- [Source: docs/epics.md#Section-Story-2.3]
- [Source: docs/architecture.md#Section-Data-Architecture]
## Code Review
- **Date**: 2025-12-11
- **Reviewer**: Antigravity
- **Status**: Approved
- **Report**: [Review Report](review-report-2-3.md)
