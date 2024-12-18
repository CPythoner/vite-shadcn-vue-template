from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import aiosqlite
from typing import List, Optional
from pydantic import BaseModel
import os

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "podcast.db")

# Pydantic 模型
class Podcast(BaseModel):
    id: int
    title: str
    description: str
    cover_url: str
    level: str
    category: str
    language: str
    author: str
    rss_url: str
    website_url: str
    episode_count: int
    latest_episode_at: str
    created_at: str
    updated_at: str
    status: str

class Episode(BaseModel):
    id: int
    podcast_id: int
    title: str
    description: str
    cover_url: Optional[str]
    audio_url: str
    duration: int
    published_at: str
    episode_number: int
    default_transcript_id: Optional[int]
    created_at: str
    updated_at: str

# API 路由
@app.get("/api/podcasts", response_model=List[Podcast])
async def get_podcasts(category: Optional[str] = None, level: Optional[str] = None):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        sql = "SELECT * FROM podcasts"
        params = []

        if category:
            sql += " WHERE category = ?"
            params.append(category)
        elif level:
            sql += " WHERE level = ?"
            params.append(level)

        sql += " ORDER BY latest_episode_at DESC"

        async with db.execute(sql, params) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

@app.get("/api/podcasts/{podcast_id}", response_model=Podcast)
async def get_podcast(podcast_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM podcasts WHERE id = ?",
            [podcast_id]
        ) as cursor:
            row = await cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Podcast not found")
            return dict(row)

@app.get("/api/podcasts/{podcast_id}/episodes", response_model=List[Episode])
async def get_podcast_episodes(podcast_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM episodes WHERE podcast_id = ? ORDER BY published_at DESC",
            [podcast_id]
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

@app.get("/api/episodes/{episode_id}", response_model=Episode)
async def get_episode(episode_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM episodes WHERE id = ?",
            [episode_id]
        ) as cursor:
            row = await cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Episode not found")
            return dict(row)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)