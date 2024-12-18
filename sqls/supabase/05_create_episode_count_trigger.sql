-- 创建更新播客集数的函数
create or replace function update_podcast_episode_count()
returns trigger as $$
begin
  if (TG_OP = 'INSERT') then
    -- 更新播客的集数和最新一集时间
    update public.podcasts
    set episode_count = episode_count + 1,
        latest_episode_at = greatest(latest_episode_at, NEW.published_at)
    where id = NEW.podcast_id;
    return NEW;
  elsif (TG_OP = 'DELETE') then
    -- 更新播客的集数
    update public.podcasts
    set episode_count = episode_count - 1,
        latest_episode_at = (
          select max(published_at)
          from public.episodes
          where podcast_id = OLD.podcast_id
        )
    where id = OLD.podcast_id;
    return OLD;
  end if;
  return null;
end;
$$ language plpgsql;

-- 创建触发器
create trigger update_podcast_episode_count
  after insert or delete on public.episodes
  for each row
  execute function update_podcast_episode_count();
