"""
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT UNIQUE NOT NULL,  -- Discord User ID
    coins INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS stats (
    user_id INTEGER PRIMARY KEY,
    stealth INTEGER NOT NULL DEFAULT 0,
    intelligent INTEGER NOT NULL DEFAULT 0,
    strength INTEGER NOT NULL DEFAULT 0,
    influence INTEGER NOT NULL DEFAULT 0,
    awarness INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS claimed (
    user_id INTEGER PRIMARY KEY,
    claimed_daily_reward BOOLEAN NOT NULL DEFAULT 0,
    claimed_weekly_reward BOOLEAN NOT NULL DEFAULT 0,
    claimed_daily_reward_how_much INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS inventory (
    user_id INTEGER,
    item_id TEXT,
    amount INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (user_id, item_id),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

)
"""