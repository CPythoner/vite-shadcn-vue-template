create table if not exists public.transcripts (
  id uuid default gen_random_uuid() primary key,
  episode_id uuid references public.episodes(id) on delete cascade not null,
  language varchar(50) not null,
  type varchar(50) not null,  -- CC字幕/完整文本/简化文本
  format varchar(50) not null,  -- srt/vtt/txt
  content text,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 创建索引
create index if not exists transcripts_episode_id_idx on public.transcripts(episode_id);
create index if not exists transcripts_language_idx on public.transcripts(language);

-- 添加更新时间触发器
create trigger set_updated_at
  before update on public.transcripts
  for each row
  execute function public.set_updated_at();

-- 添加RLS策略
alter table public.transcripts enable row level security;

-- 添加 episodes 表中的外键约束
alter table public.episodes
  add constraint episodes_default_transcript_id_fkey
  foreign key (default_transcript_id)
  references public.transcripts(id)
  on delete set null;
