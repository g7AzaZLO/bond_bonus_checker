import sqlite3
import aiohttp
import aiosqlite
import requests
import logging
from db.database import DB_PATH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_bonus_for_bond_index(api_url, target_index):
    """
    Делает запрос к API, находит бонд с заданным индексом и возвращает значение bonus.

    :param api_url: str, URL API
    :param target_index: int, индекс искомого бонда
    :return: float, значение бонуса, либо None, если бонд не найден
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        for bond in data.get("bonds", []):
            if bond.get("index") == target_index:
                return bond.get("bonus")

        return None
    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None


async def get_user_bonds(telegram_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute("""
        SELECT bond_index, target_bonus FROM user_bonds
        WHERE telegram_id = ?
        """, (telegram_id,))
        bonds = await cursor.fetchall()
        return bonds


async def delete_user_bond(telegram_id, bond_index):
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute("""
        DELETE FROM user_bonds WHERE telegram_id = ? AND bond_index = ?
        """, (telegram_id, bond_index))
        await conn.commit()
        deleted = cursor.rowcount > 0
        return deleted


async def get_all_bonds(api_url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get("bonds", [])
    except Exception as e:
        logger.error(f"Ошибка при запросе API: {e}")
        return []
