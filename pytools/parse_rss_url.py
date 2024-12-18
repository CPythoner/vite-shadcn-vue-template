import feedparser
import datetime
import sqlite3
from typing import List, Dict, Any
from pathlib import Path


class RSSParser:
    def __init__(self, rss_urls: List[str], db_path: str = "podcast.db"):
        self.rss_urls = rss_urls
        self.db_path = db_path
        self.ensure_db_exists()

    def ensure_db_exists(self):
        """确保数据库和表已创建"""
        if not Path(self.db_path).exists():
            # 读取并执行建表SQL
            sql_files = [
                'sqls/sqlite/01_create_tables.sql',
                'sqls/sqlite/02_create_triggers.sql'
            ]

            conn = sqlite3.connect(self.db_path)
            try:
                for sql_file in sql_files:
                    with open(sql_file, 'r', encoding='utf-8') as f:
                        conn.executescript(f.read())
                conn.commit()
            finally:
                conn.close()

    def insert_to_db(self, parsed_data: List[Dict[str, Any]]) -> None:
        """将解析的数据插入数据库，包含重复检查"""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()

            for data in parsed_data:
                if data["status"] != "成功":
                    print(f"跳过插入失败的数据: {data['url']}")
                    continue

                # 检查播客是否已存在
                podcast_data = data["podcast_data"]
                cursor.execute(
                    "SELECT id FROM podcasts WHERE rss_url = ?",
                    (podcast_data["rss_url"],)
                )
                existing_podcast = cursor.fetchone()

                if existing_podcast:
                    podcast_id = existing_podcast[0]
                    print(f"播客已存在: {podcast_data['title']}, 跳过插入播客信息")
                else:
                    # 插入新播客
                    cursor.execute("""
                        INSERT INTO podcasts (
                            title, description, cover_url, level, category,
                            language, author, rss_url, website_url, status
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        podcast_data["title"],
                        podcast_data["description"],
                        podcast_data["cover_url"],
                        podcast_data["level"],
                        podcast_data["category"],
                        podcast_data["language"],
                        podcast_data["author"],
                        podcast_data["rss_url"],
                        podcast_data["website_url"],
                        podcast_data["status"]
                    ))
                    podcast_id = cursor.lastrowid
                    print(f"已插入新播客: {podcast_data['title']}")

                # 处理剧集
                for episode in data["episodes_data"]:
                    # 检查剧集是否已存在
                    cursor.execute("""
                        SELECT id FROM episodes
                        WHERE podcast_id = ? AND title = ? AND published_at = ?
                    """, (
                        podcast_id,
                        episode["title"],
                        episode["published_at"]
                    ))

                    if cursor.fetchone():
                        print(f"剧集已存在: {episode['title']}, 跳过插入")
                        continue

                    # 插入新剧集
                    cursor.execute("""
                        INSERT INTO episodes (
                            podcast_id, title, description, cover_url,
                            audio_url, duration, published_at, episode_number
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        podcast_id,
                        episode["title"],
                        episode["description"],
                        episode.get("cover_url"),
                        episode["audio_url"],
                        episode["duration"],
                        episode["published_at"],
                        episode["episode_number"]
                    ))
                    print(f"已插入新剧集: {episode['title']}")

            conn.commit()
            print("数据处理完成")

        except Exception as e:
            conn.rollback()
            print(f"插入数据时出错: {str(e)}")
        finally:
            conn.close()

    def check_podcast_exists(self, cursor, rss_url: str) -> bool:
        """检查播客是否已存在"""
        cursor.execute("SELECT 1 FROM podcasts WHERE rss_url = ?", (rss_url,))
        return cursor.fetchone() is not None

    def check_episode_exists(self, cursor, podcast_id: int, title: str, published_at: str) -> bool:
        """检查剧集是否已存在"""
        cursor.execute("""
            SELECT 1 FROM episodes
            WHERE podcast_id = ? AND title = ? AND published_at = ?
        """, (podcast_id, title, published_at))
        return cursor.fetchone() is not None

    def parse(self) -> List[Dict[str, Any]]:
        results = []
        for rss_url in self.rss_urls:
            result = self.parse_single_rss(rss_url)
            results.append(result)
        return results

    def parse_single_rss(self, rss_url: str) -> Dict[str, Any]:
        feed = feedparser.parse(rss_url)
        if feed.bozo:
            return {"url": rss_url, "status": "失败", "error": "无法解析 RSS 源"}

        try:
            podcast_data = self.extract_podcast_data(feed, rss_url)
            episodes_data = [self.parse_episode(entry) for entry in feed.entries]
            return {
                "url": rss_url,
                "status": "成功",
                "podcast_data": podcast_data,
                "episodes_data": episodes_data,
            }
        except Exception as e:
            return {"url": rss_url, "status": "失败", "error": str(e)}

    def extract_podcast_data(
        self, feed: feedparser.FeedParserDict, rss_url: str
    ) -> Dict[str, Any]:
        podcast_data = {
            "title": feed.feed.get("title", "").replace("'", "''"),
            "description": feed.feed.get("description", "").replace("'", "''"),
            "cover_url": feed.feed.get("image", {}).get("href", "").replace("'", "''"),
            "level": "未知",  # 可根据需要修改
            "category": "未知",  # 可根据需要修改
            "language": feed.feed.get("language", "").replace("'", "''"),
            "author": feed.feed.get("author", "").replace("'", "''"),
            "rss_url": rss_url.replace("'", "''"),
            "website_url": feed.feed.get("link", "").replace("'", "''"),
            "episode_count": len(feed.entries),
            "latest_episode_at": self.get_latest_episode_date(feed.entries),
            "status": "active",
        }
        return podcast_data

    def get_latest_episode_date(self, entries: List[feedparser.FeedParserDict]) -> str:
        latest_date = None
        for entry in entries:
            published = entry.get("published_parsed")
            if published:
                entry_date = datetime.datetime(*published[:6])
                if not latest_date or entry_date > latest_date:
                    latest_date = entry_date
        return latest_date.strftime("%Y-%m-%d %H:%M:%S") if latest_date else None

    def parse_episode(self, entry: feedparser.FeedParserDict) -> Dict[str, Any]:
        audio_url = ""
        for link in entry.get("links", []):
            if link.get("type") in [
                "audio/x-m4a",
                "audio/mp4",
                "audio/mpeg",
            ] or link.get("href", "").endswith(".m4a"):
                audio_url = link.get("href", "").replace("'", "''")
                break

        published = entry.get("published_parsed")
        published_at = (
            datetime.datetime(*published[:6]).strftime("%Y-%m-%d %H:%M:%S")
            if published
            else None
        )

        episode_data = {
            "title": entry.get("title", "").replace("'", "''"),
            "description": entry.get("description", "").replace("'", "''"),
            "cover_url": entry.get("image", {}).get("href", "").replace("'", "''"),
            "audio_url": audio_url,
            "duration": self.duration_to_seconds(entry.get("itunes_duration", "")),
            "published_at": published_at,
            "episode_number": int(entry.get("itunes:episode", "0")),
            "default_transcript_id": None,  # 根据需要设置
        }
        return episode_data

    def duration_to_seconds(self, duration_str: str) -> int:
        if not duration_str:
            return None
        parts = duration_str.split(":")
        parts = [int(part) for part in parts]
        while len(parts) < 3:
            parts.insert(0, 0)  # 确保有小时、分钟、秒
        hours, minutes, seconds = parts
        return hours * 3600 + minutes * 60 + seconds

    def generate_sql(self, parsed_data: List[Dict[str, Any]]) -> List[str]:
        sql_statements = []
        for data in parsed_data:
            if data["status"] == "成功":
                podcast_sql = self.generate_podcast_insert_sql(data["podcast_data"])
                sql_statements.append(podcast_sql)
                for episode in data["episodes_data"]:
                    episode_sql = self.generate_episode_insert_sql(episode)
                    sql_statements.append(episode_sql)
        return sql_statements

    def generate_podcast_insert_sql(self, podcast_data: Dict[str, Any]) -> str:
        sql = f"""
        INSERT INTO podcasts (title, description, cover_url, level, category, language, author, rss_url, website_url, episode_count, latest_episode_at, status)
        VALUES ('{podcast_data["title"]}', '{podcast_data["description"]}', '{podcast_data["cover_url"]}', '{podcast_data["level"]}', '{podcast_data["category"]}', '{podcast_data["language"]}', '{podcast_data["author"]}', '{podcast_data["rss_url"]}', '{podcast_data["website_url"]}', {podcast_data["episode_count"]}, '{podcast_data["latest_episode_at"]}', '{podcast_data["status"]}');
        """
        return sql.strip()

    def generate_episode_insert_sql(self, episode_data: Dict[str, Any]) -> str:
        sql = f"""
        INSERT INTO episodes (podcast_id, title, description, cover_url, audio_url, duration, published_at, episode_number, default_transcript_id)
        VALUES (LAST_INSERT_ROWID(), '{episode_data["title"]}', '{episode_data["description"]}', '{episode_data["cover_url"]}', '{episode_data["audio_url"]}', {episode_data["duration"]}, '{episode_data["published_at"]}', {episode_data["episode_number"]}, {episode_data["default_transcript_id"]});
        """
        return sql.strip()


# 使用示例
def main():
    rss_urls = [
        "https://feeds.megaphone.fm/SONORO7201496122",
        "https://feeds.megaphone.fm/TPG4197403620",
        "https://feeds.megaphone.fm/GLSS2276105381"
    ]

    parser = RSSParser(rss_urls)

    # 解析数据
    parsed_data = parser.parse()

    # 直接插入数据库
    parser.insert_to_db(parsed_data)

    # 同时也生成SQL文件以供参考
    sql_statements = parser.generate_sql(parsed_data)
    with open('sqls/sqlite/03_insert_podcast_data.sql', 'w', encoding='utf-8') as f:
        f.write('-- 自动生成的播客数据插入语句\n\n')
        for sql in sql_statements:
            f.write(f'{sql}\n\n')


if __name__ == "__main__":
    main()
