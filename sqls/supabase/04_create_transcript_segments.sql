create table if not exists public.transcript_segments (
  id uuid default gen_random_uuid() primary key,
  transcript_id uuid references public.transcripts(id) on delete cascade not null,
  start_time numeric(10, 3) not null,  -- 精确到毫秒
  end_time numeric(10, 3) not null,
  content text not null,
  translation text,
  sequence integer not null,
  speaker varchar(255),
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 创建索引
create index if not exists transcript_segments_transcript_id_idx on public.transcript_segments(transcript_id);
create index if not exists transcript_segments_sequence_idx on public.transcript_segments(sequence);
create index if not exists transcript_segments_time_range_idx on public.transcript_segments(start_time, end_time);

-- 添加约束
alter table public.transcript_segments
  add constraint transcript_segments_time_check
  check (start_time < end_time);

-- 添加RLS策略
alter table public.transcript_segments enable row level security;
