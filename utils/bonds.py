import sqlite3

import requests

from db.database import DB_PATH


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

def get_user_bonds(telegram_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    bonds = cursor.execute("""
    SELECT bond_index, target_bonus FROM user_bonds
    WHERE telegram_id = ?
    """, (telegram_id,)).fetchall()

    conn.close()
    return bonds

def delete_user_bond(telegram_id, bond_index):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM user_bonds WHERE telegram_id = ? AND bond_index = ?
    """, (telegram_id, bond_index))

    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

def get_all_bonds(api_url):
    """
    Получает список всех бондов из API.

    :param api_url: str, URL API
    :return: list, список бондов
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data.get("bonds", [])
    except requests.RequestException as e:
        print(f"Ошибка при запросе API: {e}")
        return []