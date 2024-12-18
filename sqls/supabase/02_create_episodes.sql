create table if not exists public.episodes (
  id uuid default gen_random_uuid() primary key,
  podcast_id uuid references public.podcasts(id) on delete cascade not null,
  title varchar(255) not null,
  description text,
  audio_url text not null,
  duration integer, -- 单位：秒
  published_at timestamp with time zone not null,
  episode_number integer,
  default_transcript_id uuid,  -- 将在创建 transcripts 表后添加外键约束
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 创建索引
create index if not exists episodes_podcast_id_idx on public.episodes(podcast_id);
create index if not exists episodes_published_at_idx on public.episodes(published_at);

-- 添加更新时间触发器
create trigger set_updated_at
  before update on public.episodes
  for each row
  execute function public.set_updated_at();

-- 添加RLS策略
alter table public.episodes enable row level security;
