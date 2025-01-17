import asyncio

from aiogram import Bot
from settings import dp, bot
from db.database import init_db, get_users_to_notify

from handlers.channels import channels_router
from handlers.standart import standart_router
from handlers.bonds import bonds_router

dp.include_router(standart_router)
dp.include_router(channels_router)
dp.include_router(bonds_router)

async def notify_users(api_url, bot: Bot):
    while True:
        notifications = get_users_to_notify(api_url)
        for user_id, bond_index, bonus in notifications:
            await bot.send_message(user_id, f"Бонд {bond_index} достиг бонуса {bonus}.")
        await asyncio.sleep(300)

async def main():
    api_url = "https://realtime-api.ape.bond/bonds"
    asyncio.create_task(notify_users(api_url, bot))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    init_db()
    asyncio.run(main())
