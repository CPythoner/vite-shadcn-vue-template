-- 更新播客表的更新时间
CREATE TRIGGER IF NOT EXISTS update_podcasts_timestamp
AFTER UPDATE ON podcasts
BEGIN
  UPDATE podcasts SET updated_at = datetime('now')
  WHERE id = NEW.id;
END;

-- 更新剧集表的更新时间
CREATE TRIGGER IF NOT EXISTS update_episodes_timestamp
AFTER UPDATE ON episodes
BEGIN
  UPDATE episodes SET updated_at = datetime('now')
  WHERE id = NEW.id;
END;

-- 更新字幕表的更新时间
CREATE TRIGGER IF NOT EXISTS update_transcripts_timestamp
AFTER UPDATE ON transcripts
BEGIN
  UPDATE transcripts SET updated_at = datetime('now')
  WHERE id = NEW.id;
END;

-- 更新播客的集数和最新一集时间
CREATE TRIGGER IF NOT EXISTS update_podcast_episode_count_insert
AFTER INSERT ON episodes
BEGIN
  UPDATE podcasts
  SET
    episode_count = episode_count + 1,
    latest_episode_at = CASE
      WHEN latest_episode_at IS NULL OR NEW.published_at > latest_episode_at
      THEN NEW.published_at
      ELSE latest_episode_at
    END
  WHERE id = NEW.podcast_id;
END;

CREATE TRIGGER IF NOT EXISTS update_podcast_episode_count_delete
AFTER DELETE ON episodes
BEGIN
  UPDATE podcasts
  SET
    episode_count = episode_count - 1,
    latest_episode_at = (
      SELECT MAX(published_at)
      FROM episodes
      WHERE podcast_id = OLD.podcast_id
    )
  WHERE id = OLD.podcast_id;
END;
