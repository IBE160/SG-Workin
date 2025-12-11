-- Enable pgvector
create extension if not exists vector;

-- Create table
create table if not exists document_chunks (
    id bigserial primary key,
    url text not null,
    chunk_index integer not null,
    content text not null,
    metadata jsonb not null default '{}'::jsonb, -- Schema: { "source": "url", "title": "string", "created_at": "iso_string" }
    embedding vector(768) -- text-embedding-004 dimension
);

-- Create HNSW Index for performance
create index on document_chunks using hnsw (embedding vector_cosine_ops);

-- Enable RLS
alter table document_chunks enable row level security;

-- Policy: Allow Service Role (Backend) full access
create policy "Service Role Full Access" on document_chunks
    as permissive for all
    to service_role
    using (true)
    with check (true);

-- Policy: Allow Public Read (if needed for client-side RAG) or keep restricted to Service Role
-- For now, restrict to service_role as backend mediates RAG.
