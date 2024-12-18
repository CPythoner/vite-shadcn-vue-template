import { Database } from 'sqlite3'
import { open } from 'sqlite'

// 类型定义
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

// 数据访问类
export class PodcastService {
  private dbPromise = open({
    filename: './podcast.db',
    driver: Database
  })

  // 获取所有播客
  async getAllPodcasts(): Promise<Podcast[]> {
    const db = await this.dbPromise
    return db.all<Podcast[]>('SELECT * FROM podcasts ORDER BY latest_episode_at DESC')
  }

  // 获取单个播客
  async getPodcast(id: number): Promise<Podcast | null> {
    const db = await this.dbPromise
    const result = await db.get<Podcast>('SELECT * FROM podcasts WHERE id = ?', id)
    return result || null
  }

  // 获取播客的所有剧集
  async getEpisodes(podcastId: number): Promise<Episode[]> {
    const db = await this.dbPromise
    return db.all<Episode[]>(
      'SELECT * FROM episodes WHERE podcast_id = ? ORDER BY published_at DESC',
      podcastId
    )
  }

  // 获取单个剧集
  async getEpisode(id: number): Promise<Episode | null> {
    const db = await this.dbPromise
    const result = await db.get<Episode>('SELECT * FROM episodes WHERE id = ?', id)
    return result || null
  }

  // 按分类获取播客
  async getPodcastsByCategory(category: string): Promise<Podcast[]> {
    const db = await this.dbPromise
    return db.all<Podcast[]>('SELECT * FROM podcasts WHERE category = ?', category)
  }

  // 按级别获取播客
  async getPodcastsByLevel(level: string): Promise<Podcast[]> {
    const db = await this.dbPromise
    return db.all<Podcast[]>('SELECT * FROM podcasts WHERE level = ?', level)
  }

  // 搜索播客
  async searchPodcasts(query: string): Promise<Podcast[]> {
    const db = await this.dbPromise
    return db.all<Podcast[]>(
      'SELECT * FROM podcasts WHERE title LIKE ? OR description LIKE ?',
      [`%${query}%`, `%${query}%`]
    )
  }
}
