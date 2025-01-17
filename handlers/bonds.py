from aiogram import Router, types
from aiogram.filters import Command
from db.database import save_user_data

bonds_router = Router()

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

        save_user_data(user_id, bond_index, target_bonus)

        await message.reply(f"Данные сохранены: Бонд {bond_index}, Бонус {target_bonus}")
    except ValueError:
        await message.reply("Ошибка в формате команды. Попробуйте снова.")