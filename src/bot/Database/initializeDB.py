import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env")
DB_PATH = os.getenv("DB_PATH")

# Initializes the SQLite database and ensures required tables exist
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table for storing custom roles and boost levels
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS custom_roles (
            user_id TEXT PRIMARY KEY,
            role_id TEXT NOT NULL,
            boost_level INTEGER DEFAULT 1
        )
        """
    )

    # Create table for storing user accounts and their coin balances
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT,
            money INTEGER DEFAULT 0
        )
        """
    )

    # Insert initial bank record if not present
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, username, money) VALUES (?, ?, ?)",
        ("1371864280332501072", "Clubhall Bank", 1000000000),
    )

    # Commit changes and close the connection
    conn.commit()
    conn.close()
