import aiohttp
import aiosqlite
import logging

DB_PATH = "bot.db"

logger = logging.getLogger(__name__)

async def init_db():
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS user_bonds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            bond_index INTEGER,
            target_bonus REAL,
            UNIQUE(telegram_id, bond_index)
        )
        """)
        await conn.commit()

async def save_user_data(telegram_id, bond_index, target_bonus):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("""
        INSERT OR REPLACE INTO user_bonds (telegram_id, bond_index, target_bonus)
        VALUES (?, ?, ?)
        """, (telegram_id, bond_index, target_bonus))
        await conn.commit()

async def get_users_to_notify(api_url):
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute("SELECT telegram_id, bond_index, target_bonus FROM user_bonds")
        users = await cursor.fetchall()

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            response.raise_for_status()
            bonds = await response.json()

    notifications = []
    for user in users:
        telegram_id, bond_index, target_bonus = user
        bond = next((b for b in bonds.get("bonds", []) if b.get("index") == bond_index), None)
        if bond and bond.get("bonus") >= target_bonus:
            notifications.append((telegram_id, bond_index, bond.get("bonus")))

    return notifications