-- 创建播客表
CREATE TABLE IF NOT EXISTS podcasts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  cover_url TEXT,
  level TEXT NOT NULL,  -- 初级/中级/高级
  category TEXT NOT NULL, -- 听力练习/口语练习/新闻/故事等
  language TEXT NOT NULL,
  author TEXT,
  rss_url TEXT,
  website_url TEXT,
  episode_count INTEGER DEFAULT 0,
  latest_episode_at TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  status TEXT NOT NULL DEFAULT 'active'
);

-- 创建剧集表
CREATE TABLE IF NOT EXISTS episodes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  podcast_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  cover_url TEXT,
  audio_url TEXT NOT NULL,
  duration INTEGER,  -- 单位：秒
  published_at TEXT NOT NULL,
  episode_number INTEGER,
  default_transcript_id INTEGER,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (podcast_id) REFERENCES podcasts(id) ON DELETE CASCADE
);

-- 创建字幕表
CREATE TABLE IF NOT EXISTS transcripts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  episode_id INTEGER NOT NULL,
  language TEXT NOT NULL,
  type TEXT NOT NULL,  -- CC字幕/完整文本/简化文本
  format TEXT NOT NULL,  -- srt/vtt/txt
  content TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (episode_id) REFERENCES episodes(id) ON DELETE CASCADE
);

-- 创建字幕片段表
CREATE TABLE IF NOT EXISTS transcript_segments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  transcript_id INTEGER NOT NULL,
  start_time REAL NOT NULL,  -- 精确到毫秒
  end_time REAL NOT NULL,
  content TEXT NOT NULL,
  translation TEXT,
  sequence INTEGER NOT NULL,
  speaker TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (transcript_id) REFERENCES transcripts(id) ON DELETE CASCADE,
  CHECK (start_time < end_time)
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_podcasts_level ON podcasts(level);
CREATE INDEX IF NOT EXISTS idx_podcasts_category ON podcasts(category);
CREATE INDEX IF NOT EXISTS idx_podcasts_language ON podcasts(language);
CREATE INDEX IF NOT EXISTS idx_podcasts_latest_episode ON podcasts(latest_episode_at);

CREATE INDEX IF NOT EXISTS idx_episodes_podcast ON episodes(podcast_id);
CREATE INDEX IF NOT EXISTS idx_episodes_published ON episodes(published_at);

CREATE INDEX IF NOT EXISTS idx_transcripts_episode ON transcripts(episode_id);
CREATE INDEX IF NOT EXISTS idx_transcripts_language ON transcripts(language);

CREATE INDEX IF NOT EXISTS idx_segments_transcript ON transcript_segments(transcript_id);
CREATE INDEX IF NOT EXISTS idx_segments_sequence ON transcript_segments(sequence);
CREATE INDEX IF NOT EXISTS idx_segments_time ON transcript_segments(start_time, end_time);
