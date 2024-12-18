export interface Podcast {
  id: number
  title: string
  description: string
  cover_url: string
  level: string
  category: string
  language: string
  author: string
  rss_url: string
  website_url: string
  episode_count: number
  latest_episode_at: string
  created_at: string
  updated_at: string
  status: string
}

export interface Episode {
  id: number
  podcast_id: number
  title: string
  description: string
  cover_url: string | null
  audio_url: string
  duration: number
  published_at: string
  episode_number: number
  default_transcript_id: number | null
  created_at: string
  updated_at: string
}
