import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env")
DB_PATH = os.getenv("DB_PATH")

# Internal helper to fetch a single row from a query
def _fetchone(query: str, params=()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()
    return row

# Internal helper to execute a query with optional parameters (no result expected)
def _execute(query: str, params=()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

# Registers a new user if not already present in the database
def register_user(user_id: str, username: str):
    if not _fetchone("SELECT 1 FROM users WHERE user_id = ?", (user_id,)):
        _execute(
            "INSERT INTO users (user_id, username, money) VALUES (?, ?, ?)",
            (user_id, username, 5),  # Initial balance: 5 coins
        )

# Retrieves the custom role ID associated with a user
def get_custom_role(user_id: str):
    row = _fetchone("SELECT role_id FROM custom_roles WHERE user_id = ?", (user_id,))
    return int(row[0]) if row else None

# Sets or updates a user's custom role ID
def set_custom_role(user_id: str, role_id: int):
    _execute(
        """
        INSERT OR REPLACE INTO custom_roles (user_id, role_id)
        VALUES (?, ?)
        """,
        (user_id, role_id),
    )

# Deletes a user's custom role entry
def delete_custom_role(user_id: str):
    _execute("DELETE FROM custom_roles WHERE user_id = ?", (user_id,))

# Retrieves a user's boost level (defaults to 1 if not set)
def get_boost_level(user_id: str) -> int:
    row = _fetchone(
        "SELECT boost_level FROM custom_roles WHERE user_id = ?", (user_id,)
    )
    return row[0] if row else 1

# Updates a user's boost level
def set_boost_level(user_id: str, level: int):
    _execute(
        "UPDATE custom_roles SET boost_level = ? WHERE user_id = ?", (level, user_id)
    )

# Gets a user's current coin balance
def get_money(user_id: str) -> int:
    row = _fetchone("SELECT money FROM users WHERE user_id = ?", (user_id,))
    return row[0] if row else 0

# Sets a user's coin balance directly
def set_money(user_id: str, amount: int):
    _execute("UPDATE users SET money = ? WHERE user_id = ?", (amount, user_id))
