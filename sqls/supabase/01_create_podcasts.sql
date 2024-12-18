create table if not exists public.podcasts (
  id uuid default gen_random_uuid() primary key,
  title varchar(255) not null,
  description text,
  cover_url text,
  level varchar(50) not null,  -- 初级/中级/高级
  category varchar(50) not null, -- 听力练习/口语练习/新闻/故事等
  language varchar(50) not null,
  author varchar(255),
  rss_url text,
  website_url text,
  episode_count integer default 0,  -- 添加总集数字段
  latest_episode_at timestamp with time zone,  -- 添加最新一集发布时间
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null,
  status varchar(50) default 'active' not null
);

-- 创建索引
create index if not exists podcasts_level_idx on public.podcasts(level);
create index if not exists podcasts_category_idx on public.podcasts(category);
create index if not exists podcasts_language_idx on public.podcasts(language);
create index if not exists podcasts_latest_episode_at_idx on public.podcasts(latest_episode_at);

-- 添加更新时间触发器
create trigger set_updated_at
  before update on public.podcasts
  for each row
  execute function public.set_updated_at();

-- 添加RLS策略
alter table public.podcasts enable row level security;
