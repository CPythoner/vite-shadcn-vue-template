import sqlite3
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_database():
    db_path = os.path.join(os.path.dirname(__file__), "..", "podcast.db")

    if not os.path.exists(db_path):
        logger.error(f"Database file not found: {db_path}")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        logger.info(f"Found tables: {[table[0] for table in tables]}")

        # 检查是否有数据
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            logger.info(f"Table {table[0]} has {count} rows")

        conn.close()
        return True
    except Exception as e:
        logger.error(f"Database check failed: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    check_database()
