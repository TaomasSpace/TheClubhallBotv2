import sqlite3
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
DB_PATH = os.getenv("DB_PATH")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS custom_roles (
        user_id TEXT PRIMARY KEY,
        role_id TEXT NOT NULL,
        boost_level INTEGER DEFAULT 1
    )
    """
    )

    conn.commit()
    conn.close()
