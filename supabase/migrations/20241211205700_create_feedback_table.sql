-- Create feedback table
create table if not exists public.feedback (
  id uuid default gen_random_uuid() primary key,
  rating integer not null check (rating >= 1 and rating <= 10),
  comment text,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Enable RLS
alter table public.feedback enable row level security;

-- Create policy to allow anonymous inserts (since chat is public)
-- Adjust based on auth requirements. For now, we assume anyone can submit feedback.
create policy "Enable insert for all users" on public.feedback
  for insert with check (true);

-- Create policy to allow service role to read/manage
create policy "Enable read for service role only" on public.feedback
  for select using (auth.role() = 'service_role');
