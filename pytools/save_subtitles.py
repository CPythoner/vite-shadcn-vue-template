import sqlite3
import re
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_time(time_str: str) -> float:
    """
    将时间字符串转换为秒数
    例如: "00:00:05.200" -> 5.2
    """
    # 分离时分秒和毫秒
    main_time, ms = time_str.split('.')
    h, m, s = main_time.split(':')

    # 转换为秒
    total_seconds = (
        int(h) * 3600 +  # 小时转秒
        int(m) * 60 +    # 分钟转秒
        int(s)           # 秒
    )

    # 添加毫秒部分（转换为秒的小数部分）
    total_seconds += int(ms) / 1000

    return total_seconds

def parse_vtt(vtt_file: str) -> list[tuple]:
    """
    解析 VTT 文件，返回字幕数据列表
    """
    subtitles = []
    with open(vtt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 跳过 WEBVTT 头部
    lines = [line.strip() for line in lines[2:]]

    current_time = None
    current_text = []

    time_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})')

    for line in lines:
        if not line:
            if current_time and current_text:
                start_time, end_time = current_time
                text = ' '.join(current_text)
                subtitles.append((start_time, end_time, text))
                current_text = []
            continue

        time_match = time_pattern.match(line)
        if time_match:
            if current_time and current_text:
                start_time, end_time = current_time
                text = ' '.join(current_text)
                subtitles.append((start_time, end_time, text))
                current_text = []

            start_str, end_str = time_match.groups()
            current_time = (parse_time(start_str), parse_time(end_str))
        elif line:
            text = line.lstrip('- ').strip()
            if text:
                current_text.append(text)

    # 处理最后一段字幕
    if current_time and current_text:
        start_time, end_time = current_time
        text = ' '.join(current_text)
        subtitles.append((start_time, end_time, text))

    return subtitles

def save_subtitles_to_db(vtt_file: str, episode_id: int, db_path: str) -> None:
    """
    将字幕保存到数据库

    Args:
        vtt_file: VTT 文件路径
        episode_id: 对应的剧集 ID
        db_path: 数据库文件路径
    """
    try:
        # 解析字幕文件
        subtitles = parse_vtt(vtt_file)

        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 创建字幕表（如果不存在）
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS subtitles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            episode_id INTEGER NOT NULL,
            start_time FLOAT NOT NULL,
            end_time FLOAT NOT NULL,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (episode_id) REFERENCES episodes(id)
        )
        ''')

        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_subtitles_episode_id ON subtitles(episode_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_subtitles_start_time ON subtitles(start_time)')

        # 删除该剧集的现有字幕
        cursor.execute('DELETE FROM subtitles WHERE episode_id = ?', (episode_id,))

        # 插入新字幕
        cursor.executemany(
            '''INSERT INTO subtitles
                (episode_id, start_time, end_time, text)
                VALUES (?, ?, ?, ?)
             ''',
            [(episode_id, start, end, text) for start, end, text in subtitles]
        )

        # 提交事务
        conn.commit()
        logger.info(f"成功保存 {len(subtitles)} 条字幕")

    except Exception as e:
        logger.error(f"保存字幕失败: {str(e)}")
        conn.rollback()
        raise
    finally:
        conn.close()

def main():
    import argparse

    parser = argparse.ArgumentParser(description='将 VTT 字幕保存到数据库')
    parser.add_argument('vtt_file', help='VTT 文件路径')
    parser.add_argument('episode_id', type=int, help='剧集 ID')
    parser.add_argument('--db', default='podcast.db', help='数据库文件路径')

    args = parser.parse_args()
    save_subtitles_to_db(args.vtt_file, args.episode_id, args.db)

if __name__ == '__main__':
    main()
