import sqlite3
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
DB_PATH = os.getenv("DB_PATH")

# Erwartete Spalten in der users-Tabelle
EXPECTED_USER_COLUMNS = {
    "user_id": "TEXT PRIMARY KEY",
    "username": "TEXT",
    "money": "INTEGER DEFAULT 0",
    "stat_points": "INTEGER DEFAULT 0",
    "intelligence": "INTEGER DEFAULT 1",
    "strength": "INTEGER DEFAULT 1",
    "stealth": "INTEGER DEFAULT 1",
    "influence": "INTEGER DEFAULT 1",
    "awareness": "INTEGER DEFAULT 1",
}


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabelle 'custom_roles' erstellen
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS custom_roles (
            user_id TEXT PRIMARY KEY,
            role_id TEXT NOT NULL,
            boost_level INTEGER DEFAULT 1
        )
    """
    )

    # Tabelle 'users' erstellen (wenn sie noch nicht existiert)
    existing_columns = []
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT,
            money INTEGER DEFAULT 0
        )
    """
    )

    # Bestehende Spalten abrufen
    cursor.execute("PRAGMA table_info(users)")
    existing_columns = [col[1] for col in cursor.fetchall()]

    # Fehlende Spalten ergänzen
    for column_name, column_def in EXPECTED_USER_COLUMNS.items():
        if column_name not in existing_columns:
            print(f"➕ Adding missing column: {column_name}")
            cursor.execute(f"ALTER TABLE users ADD COLUMN {column_name} {column_def}")

    # Sicherstellen, dass der Bank-User existiert
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, username, money) VALUES (?, ?, ?)",
        ("1371864280332501072", "Clubhall Bank", 1000000000),
    )

    conn.commit()
    conn.close()
