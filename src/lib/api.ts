import type { Podcast, Episode } from './types'

const API_BASE_URL = '/api'

interface Subtitle {
  id: number;
  start_time: number;
  end_time: number;
  text: string;
}

export class PodcastAPI {
  // 获取所有播客
  async getAllPodcasts(): Promise<Podcast[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/podcasts`)
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to fetch podcasts')
      }
      return response.json()
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  }

  // 获取单个播客
  async getPodcast(id: number): Promise<Podcast> {
    try {
      const response = await fetch(`${API_BASE_URL}/podcasts/${id}`)
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to fetch podcast')
      }
      return response.json()
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  }

  // 获取播客的所有剧集
  async getEpisodes(podcastId: number): Promise<Episode[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/podcasts/${podcastId}/episodes`)
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to fetch episodes')
      }
      return response.json()
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  }

  // 获取单个剧集
  async getEpisode(id: number): Promise<Episode> {
    try {
      const response = await fetch(`${API_BASE_URL}/episodes/${id}`)
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to fetch episode')
      }
      return response.json()
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  }

  // 按分类获取播客
  async getPodcastsByCategory(category: string): Promise<Podcast[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/podcasts?category=${encodeURIComponent(category)}`)
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to fetch podcasts')
      }
      return response.json()
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  }

  // 按级别获取播客
  async getPodcastsByLevel(level: string): Promise<Podcast[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/podcasts?level=${encodeURIComponent(level)}`)
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to fetch podcasts')
      }
      return response.json()
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  }

  // 获取剧集字幕
  async getEpisodeSubtitles(episodeId: number): Promise<Subtitle[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/episodes/${episodeId}/subtitles`)
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to fetch subtitles')
      }
      return response.json()
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  }
}
