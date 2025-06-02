import sqlite3
import os
from dotenv import load_dotenv
import configparser
from pathlib import Path

CONFIG_PATH = Path(__file__).parents[1] / "config.ini"
config = configparser.ConfigParser()
config.optionxform = str  # nur relevant bei keys mit Groß-/Kleinschreibung
if CONFIG_PATH.is_file():
    config.read(CONFIG_PATH)

STAT_NAMES = [
    stat.strip().lower() for stat in config["Gameconfigs"]["STAT_NAMES"].split(",")
]

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
            """
            INSERT INTO users (
                user_id, username, money, stat_points,
                intelligence, strength, stealth, influence, awareness
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                username,
                5,
                0,
                1,
                1,
                1,
                1,
                1,
            ),
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


def add_stat_points(user_id: str, delta: int):
    _execute(
        "UPDATE users SET stat_points = stat_points + ? WHERE user_id = ?",
        (delta, user_id),
    )


# Gets a user's current coin balance
def get_money(user_id: str) -> int:
    row = _fetchone("SELECT money FROM users WHERE user_id = ?", (user_id,))
    return row[0] if row else 0


# Sets a user's coin balance directly
def set_money(user_id: str, amount: int):
    _execute("UPDATE users SET money = ? WHERE user_id = ?", (amount, user_id))


def get_stats(user_id: str):
    columns = STAT_NAMES + ["stat_points"]
    query = f"SELECT {', '.join(columns)} FROM users WHERE user_id = ?"
    row = _fetchone(query, (user_id,))
    if not row:
        return {s: 1 for s in STAT_NAMES} | {"stat_points": 0}
    raw = dict(zip(columns, row))
    return {
        k: (v if v is not None else (0 if k == "stat_points" else 1))
        for k, v in raw.items()
    }


def increase_stat(user_id: str, stat: str, amount: int):
    if stat not in STAT_NAMES:
        raise ValueError("invalid stat")
    _execute(
        f"UPDATE users SET {stat} = {stat} + ?, stat_points = stat_points - ? WHERE user_id = ?",
        (amount, amount, user_id),
    )
