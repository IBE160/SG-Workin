# Story 2.2: University Website Scraper

Status: Done

## Code Review
- **Date**: 2025-12-11
- **Reviewer**: Antigravity
- **Status**: Approved
- **Report**: [Review Report](review-report-2-2.md)

## Story

As a developer,
I want to build a web scraper that extracts content from the HiMolde study programs,
So that the content can be used to build the chatbot's knowledge base.

## Acceptance Criteria

1.  **Given** the target URL `https://www.himolde.no/studier/programmer/`,
2.  **When** the scraper is triggered via API,
3.  **Then** it robustly fetches the main listing page using a polite `User-Agent`.
4.  **And** it navigates to each detail program page (e.g., `/studier/programmer/it-og-digitalisering/index.html`).
5.  **And** for each program, it extracts:
    -   Program Name
    -   Brief Description
    -   Deep Content (e.g., "Fakta om programmet", "Hva lærer du?", "Oppbygging")
6.  **And** returns the aggregated, cleaned data in a structured JSON format.
7.  **And** implements retry logic (min 3 attempts) for network robustness.

## Tasks / Subtasks

- [ ] Task 1: Scraper Setup
    - [ ] Subtask 1.1: Install scraping dependencies (`beautifulsoup4`, `requests`, `tenacity`).
    - [ ] Subtask 1.2: Create `backend/services/scraper.py` with a `ScraperService` class.
    - [ ] Subtask 1.3: Configure "Polite" Request Headers (User-Agent, etc.) and Retry Logic (`tenacity`).

- [ ] Task 2: Crawling & Extraction Logic
    - [ ] Subtask 2.1: Implement `fetch_program_list()` to get all program URLs from the main page.
    - [ ] Subtask 2.2: Implement `fetch_program_details(url)` to scrape "Deep" content from each program page.
        -   *Note: Should follow internal links like "Hva lærer du" if content is fragmented, or scrape the main index content if sufficient.*
    - [ ] Subtask 2.3: Implement text cleaning (remove nav, footer, script tags).

- [ ] Task 3: API Integration
    - [ ] Subtask 3.1: Create endpoint `POST /api/scrape` in `backend/routers/scraper.py`.
    - [ ] Subtask 3.2: Connect endpoint to `ScraperService` (triggering the full crawl).
    - [ ] Subtask 3.3: Verify via `curl` that data is returned correctly.

## Dev Notes

-   **Target URL**: `https://www.himolde.no/studier/programmer/`.
-   **Deep Scraping Strategy**: The main program page seems to link to sub-pages (e.g., `.../hva-lerer-du/`). The scraper should ideally follow these critical sub-links to get a complete picture, or at least scrape the main `index.html` content fully.
    -   *Constraint*: To keep MVP simple, start by scraping the content available on the program's `index.html` + `hva-lerer-du` page if easily linkable.
-   **Robots/User-Agent**: Use `User-Agent: ibe160-chatbot-student-project` to be transparent.
-   **Performance**: Scraping 50+ pages might take time. The API endpoint should likely run this as a background task (Story 2.3 handles storage, but this story focuses on *getting* the data). For now, a sync endpoint is fine if it takes <30s, otherwise consider `BackgroundTasks`.

## References

- [Source: docs/epics.md#Section-Story-2.2]
- [Source: docs/architecture.md#Section-Epic-2]
