import * as sqlite3 from 'sqlite3'
import { open } from 'sqlite'
import * as fs from 'fs/promises'
import * as path from 'path'

// 创建数据库连接
export async function openDb() {
  return open({
    filename: path.resolve(process.cwd(), 'podcast.db'),
    driver: sqlite3.Database
  })
}

// 初始化数据库
export async function initDb() {
  const db = await openDb()

  // 读取并执行 SQL 文件
  const createTables = await fs.readFile(
    path.resolve(process.cwd(), 'sqls/sqlite/01_create_tables.sql'),
    'utf-8'
  )
  const createTriggers = await fs.readFile(
    path.resolve(process.cwd(), 'sqls/sqlite/02_create_triggers.sql'),
    'utf-8'
  )

  await db.exec(createTables)
  await db.exec(createTriggers)

  return db
}

// 数据库类型定义
export interface Podcast {
  id: number
  title: string
  description: string | null
  cover_url: string | null
  level: string
  category: string
  language: string
  author: string | null
  rss_url: string | null
  website_url: string | null
  episode_count: number
  latest_episode_at: string | null
  created_at: string
  updated_at: string
  status: string
}

// 数据库操作函数
export async function getPodcasts() {
  const db = await openDb()
  try {
    return await db.all<Podcast[]>('SELECT * FROM podcasts ORDER BY latest_episode_at DESC')
  } finally {
    await db.close()
  }
}

export async function getPodcast(id: number) {
  const db = await openDb()
  try {
    return await db.get<Podcast>('SELECT * FROM podcasts WHERE id = ?', id)
  } finally {
    await db.close()
  }
}

export async function createPodcast(podcast: Omit<Podcast, 'id' | 'created_at' | 'updated_at' | 'episode_count' | 'latest_episode_at'>) {
  const db = await openDb()
  try {
    const result = await db.run(`
      INSERT INTO podcasts (
        title, description, cover_url, level, category,
        language, author, rss_url, website_url, status
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `, [
      podcast.title,
      podcast.description,
      podcast.cover_url,
      podcast.level,
      podcast.category,
      podcast.language,
      podcast.author,
      podcast.rss_url,
      podcast.website_url,
      podcast.status || 'active'
    ])
    return result.lastID
  } finally {
    await db.close()
  }
}
