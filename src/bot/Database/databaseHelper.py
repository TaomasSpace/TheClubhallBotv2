import sqlite3

def _fetchone(query: str, params=()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()
    return row


def _execute(query: str, params=()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def register_user(user_id: str, username: str):
    if not _fetchone("SELECT 1 FROM users WHERE user_id = ?", (user_id,)):
        _execute(
            "INSERT INTO users (user_id, username) VALUES (?,?)",
            (user_id, username, 5),
        )

def get_custom_role(user_id: str):
    row = _fetchone("SELECT role_id FROM custom_roles WHERE user_id = ?", (user_id,))
    return int(row[0]) if row else None


def set_custom_role(user_id: str, role_id: int):
    _execute(
        """
    INSERT OR REPLACE INTO custom_roles (user_id, role_id)
    VALUES (?, ?)
    """,
        (user_id, role_id),
    )


def delete_custom_role(user_id: str):
    _execute("DELETE FROM custom_roles WHERE user_id = ?", (user_id,))

def get_boost_level(user_id: str) -> int:
    row = _fetchone(
        "SELECT boost_level FROM custom_roles WHERE user_id = ?", (user_id,)
    )
    return row[0] if row else 1


def set_boost_level(user_id: str, level: int):
    _execute(
        "UPDATE custom_roles SET boost_level = ? WHERE user_id = ?", (level, user_id)
    )