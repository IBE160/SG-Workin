# Story 2.5: Admin Dashboard & Tools

## Story
**As an** administrator,
**I want to** use a web interface to manage scraper targets and administrative users,
**So that** I can maintain the knowledge base and control access to the system.

## Acceptance Criteria
### Scraper Management
- [AC-1] **Dashboard**: `/admin` page lists existing scraped URLs with status/timestamps.
- [AC-2] **Add URL**: Input field to add and immediately scrape a new URL.
- [AC-3] **Scrape Action**: Triggers backend scraping and feedback (Success/Error).

### Admin User Management
- [AC-4] **User List**: List all admin users.
- [AC-5] **Add Admin**: Form to add a new admin (Email, Password).
- [AC-6] **Delete Admin**: Button to remove an admin user.
- [AC-7] **Reset Password**: Button to trigger password reset email (via Supabase Auth).

## Tasks/Subtasks
- [x] **Backend: Scraper API**
    - [x] Create `routers/admin.py` with `POST /scrape`.
    - [x] Implement `GET /urls` to list scraped (distinct) URLs.
    - [x] Register admin router in `main.py`.
    - [x] Test Scraper API endpoints.
- [x] **Backend: User Management API**
    - [x] Implement `GET /users` in `admin.py` (Supabase Service Role).
    - [x] Implement `POST /users` to create admin.
    - [x] Implement `DELETE /users/{id}`.
    - [x] Test User API endpoints.
- [x] **Frontend: Admin Dashboard**
    - [x] Create `app/admin/page.tsx` layout.
    - [x] Create `components/admin/UrlManager.tsx` (Add/List/Scrape).
    - [x] Create `components/admin/UserManager.tsx` (Add/List/Delete).
    - [x] Integrate components into main admin page.
    - [x] Verify Frontend-Backend integration.

## Dev Notes
### Implementation Plan
- **Backend**: Use `SUPABASE_SERVICE_ROLE_KEY` for user management operations. Ensure `admin.py` router is properly secured (or noted as pending security).
- **Frontend**: Use Shadcn UI components for consistent look.
    - `UrlManager`: Table for URLs, Form for adding.
    - `UserManager`: Table for Users, Form for adding.
- **Dependencies**: `supabase-admin` (or just use `supabase-js` with service role key) for backend user management.

## Dev Agent Record
### Debug Log
- [Frontend Login] Login failed initially with "Invalid API key". Found `.env.local` had concatenated lines. Fixed via split. Login/Dashboard verified afterwards.
### Completion Notes
- Implemented `Backend Scraper API` (admin.py)
- Implemented `Backend User Management API` (admin.py)
- Implemented `Frontend Admin Dashboard` (page.tsx, UrlManager.tsx, UserManager.tsx)
- Verified with unit tests (backend) and browser subagent (frontend).

## File List
- backend/routers/admin.py
- backend/tests/routers/test_admin.py
- backend/main.py
- frontend/app/admin/page.tsx
- frontend/app/layout.tsx
- frontend/components/admin/UrlManager.tsx
- frontend/components/admin/UserManager.tsx
- frontend/.env.local (Fixed)

## Change Log
- 2025-12-15: Initial implementation of Admin Dashboard and API.
- 2025-12-15: [Code Review Fix] Secured API with Auth dependency, added Password Reset, updated docs.

## Status
Ready for Review
