# Validation Report: Story 2.1 - Supabase Vector Database Setup

## 🚨 CRITICAL ISSUES (Must Fix)
1.  **Missing Indexing Strategy**: The story creates the `embedding` column but misses the critical step of creating a vector index (HNSW or IVFFlat). Without this, vector search performance will degrade significantly.
    *   *Action*: Add subtask to execute `CREATE INDEX ON document_chunks USING hnsw (embedding vector_cosine_ops);`.
2.  **Missing RLS Security**: The story creates the `document_chunks` table but fails to define Row Level Security (RLS) policies. This leaves the table potentially exposed.
    *   *Action*: Add subtask to enable RLS and define policies (e.g., generic read access, service-role only write access).
3.  **Ambiguous Embedding Model**: The instruction to "verify exact dimension" leaves execution ambiguous.
    *   *Action*: Explicitly specify the use of `text-embedding-004` with dimension `768` (standard for Gemini) to remove guesswork.

## ⚡ ENHANCEMENT OPPORTUNITIES (Should Add)
1.  **Metadata Schema Definition**: The `metadata` JSONB column is undefined.
    *   *Action*: Define a recommended schema (e.g., `{ "source_url": string, "title": string, "created_at": iso_string }`) for consistency.
2.  **Explicit Environment Variables**: While `config.py` update is mentioned, explicitly listing `SUPABASE_SERVICE_ROLE_KEY` (for backend writes) vs `SUPABASE_KEY` avoids confusion.
    *   *Action*: Add list of required new environment variables.

## ✨ OPTIMIZATIONS (Nice to Have)
1.  **Direct SQL vs Migration**: For this MVP phase, using the Supabase SQL Editor for the initial schema setup is faster than setting up a full Alembic migration chain if one doesn't exist.
    *   *Action*: Explicitly allow/prioritize using Supabase Dashboard SQL Editor for the setup task to speed up "Story 2.1".

## 🤖 LLM OPTIMIZATION
- **Make instructions directive**: Change "Verify..." to "Implement..."
- **Consolidate Tasks**: Group SQL actions.
