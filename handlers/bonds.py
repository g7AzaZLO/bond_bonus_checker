from aiogram import Router, types
from aiogram.filters import Command
import logging
from db.database import save_user_data
from settings import BOND_API
from utils.bonds import get_user_bonds, delete_user_bond, get_all_bonds

bonds_router = Router()
logger = logging.getLogger(__name__)

@bonds_router.message(Command("setbond"))
async def set_bond(message: types.Message):
    try:
        args = message.text.split()
        if len(args) != 3:
            await message.reply("Используйте: /setbond <индекс бонда> <цель бонуса>")
            return

        bond_index = int(args[1])
        target_bonus = float(args[2])
        user_id = message.from_user.id

        await save_user_data(user_id, bond_index, target_bonus)

        await message.reply(f"Добавлено уведомление: Бонд {bond_index}, Цель бонуса {target_bonus}")
    except ValueError as e:
        logger.error(f"Ошибка в команде /setbond: {e}")
        await message.reply("Ошибка в формате команды. Попробуйте снова.")

@bonds_router.message(Command("listbonds"))
async def list_bonds(message: types.Message):
    user_id = message.from_user.id
    bonds = await get_user_bonds(user_id)  # Используем await, так как функция асинхронная

    if not bonds:
        await message.reply("У вас нет активных уведомлений.")
        return

    response = "\n".join([f"{bond[0]}: {bond[1]}%" for bond in bonds])
    await message.reply(f"Ваши уведомления:\n{response}")

@bonds_router.message(Command("deletebond"))
async def delete_bond(message: types.Message):
    try:
        args = message.text.split()
        if len(args) != 2:
            await message.reply("Используйте: /deletebond <индекс бонда>")
            return

        bond_index = int(args[1])
        user_id = message.from_user.id

        deleted = await delete_user_bond(user_id, bond_index)

        if deleted:
            await message.reply(f"Уведомление на бонд {bond_index} удалено.")
        else:
            await message.reply(f"Уведомление на бонд {bond_index} не найдено.")
    except ValueError as e:
        logger.error(f"Ошибка в команде /deletebond: {e}")
        await message.reply("Ошибка в формате команды. Попробуйте снова.")

@bonds_router.message(Command("allbonds"))
async def list_all_bonds(message: types.Message):
    try:
        bonds = await get_all_bonds(BOND_API)

        if not bonds:
            await message.reply("Не удалось получить данные о бондах. Попробуйте позже.")
            return

        response = "\n".join([
            f"{bond['index']} {bond['payoutTokenName']} за {bond['principalTokenName']}"
            for bond in bonds
        ])

        await message.reply(f"Список доступных бондов:\n{response}")
    except Exception as e:
        logger.error(f"Ошибка в команде /allbonds: {e}")
        await message.reply("Произошла ошибка при получении списка бондов. Попробуйте позже.")