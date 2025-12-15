# Production Environment Variables

These variables **MUST** be set in the Vercel Project Settings (Settings -> Environment Variables).
**DO NOT COMMIT** these values to Git.

## Supabase (Database & Vector Store)

| Variable | Description | Source |
| :--- | :--- | :--- |
| `SUPABASE_URL` | The REST URL of your Supabase project. | Supabase Dashboard -> Project Settings -> API |
| `SUPABASE_KEY` | The "anon" public key. Used for client-side functionality. | Supabase Dashboard -> Project Settings -> API |
| `SUPABASE_SERVICE_ROLE_KEY` | The "service_role" secret key. Used by the Backend to bypass RLS for scraping/ingesting. **CRITICAL SECURITY**. | Supabase Dashboard -> Project Settings -> API |
| `DATABASE_URL` | The PostgreSQL Connection String (Transaction Pooler recommended for Serverless). format: `postgres://[user]:[password]@[host]:6543/[db]?pgbouncer=true` | Supabase Dashboard -> Project Settings -> Database |

## Google Gemini (AI Model)

| Variable | Description | Source |
| :--- | :--- | :--- |
| `GOOGLE_API_KEY` | API Key for Gemini 2.5 Pro. | Google AI Studio |

## Application Config

| Variable | Description | Default / Example |
| :--- | :--- | :--- |
| `ALLOWED_ORIGINS` | CORS allowed domains. Add your **Production URL** and any Preview URLs. | `https://ibe160-chatbot.vercel.app,https://ibe160-chatbot-*.vercel.app,http://localhost:3000` |
| `PROJECT_NAME` | Name of the project. | `ibe160-chatbot` |
| `GEMINI_MODEL` | The specific model version to use. | `models/gemini-2.0-flash` |
| `NEXT_PUBLIC_API_URL` | Base URL for API calls. Use relative path for Vercel Monorepo. | `/api` |
