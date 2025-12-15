# Story 4.3: Performance & Scalability Testing

## Story
**As a** developer,
**I want to** test the performance and scalability of the deployed application,
**So that** I can ensure it meets the non-functional requirements.

## Acceptance Criteria
### Performance Metrics
- [AC-1] **Response Time**: P95 response time is under 2 seconds for chat endpoints.
- [AC-2] **Concurrency**: Application handles 50 concurrent users without error.
- [AC-3] **Stability**: Error rate remains under 1% during load testing.

### Test Scenarios
- [AC-4] **Chat Load**: Simulate users sending messages to `/api/chat`.
- [AC-5] **Concurrent Access**: Multiple users engaging in conversation simultaneously.

## Tasks/Subtasks
- [ ] **Setup Testing Environment**
    - [ ] Install `locust` (Python load testing tool).
    - [ ] Configure `locustfile.py` with chat scenarios.
- [ ] **Run Baseline Tests**
    - [ ] Run test with 1 user (Baseline latency).
    - [ ] Run test with 10 concurrent users.
- [ ] **Run Scalability Tests**
    - [ ] Ramp up to 50 concurrent users.
    - [ ] Record P95 response times and error rates.
    - [ ] Generate Performance Report (`docs/performance-report.md`).
- [ ] **Optimization (If needed)**
    - [ ] Identify bottlenecks (db, external api, code).
    - [ ] Implement fixes if ACs are missing.

## Dev Notes
### Implementation Plan
- **Tools**: Use `locust` for its Python-based scripting and easy web UI.
- **Scenarios**:
    - `UserBehavior`:
        - Login (optional, or mock auth)
        - Send "Hei" (Warmup)
        - Send "Hvilke studier har dere?" (RAG intensive)
        - Send "Fortell om logistikk" (RAG intensive)
- **Target**: Run locally first. If possible/needed, run against deployed Vercel instance (caution with quotas).
- **Mocking**: For pure backend throughput, we might mock the Gemini API to test our own overhead vs external dependency latency. However, for "Real User Experience", we should test the full stack including Gemini call.

## Status
Drafted
