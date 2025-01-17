import sqlite3

DB_PATH = "bot.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        bond_index INTEGER,
        target_bonus REAL
    )
    """)
    conn.commit()
    conn.close()


def save_user_data(telegram_id, bond_index, target_bonus):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO users (telegram_id, bond_index, target_bonus)
    VALUES (?, ?, ?)
    """, (telegram_id, bond_index, target_bonus))

    conn.commit()
    conn.close()


def get_users_to_notify(api_url):
    import requests

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    users = cursor.execute("SELECT telegram_id, bond_index, target_bonus FROM users").fetchall()
    conn.close()

    response = requests.get(api_url)
    response.raise_for_status()
    bonds = response.json().get("bonds", [])

    notifications = []
    for user in users:
        telegram_id, bond_index, target_bonus = user
        bond = next((b for b in bonds if b.get("index") == bond_index), None)
        if bond and bond.get("bonus") >= target_bonus:
            notifications.append((telegram_id, bond_index, bond.get("bonus")))

    return notifications
