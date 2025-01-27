import asyncio
from datetime import datetime
import logging

from aiogram import Bot
from settings import dp, bot, BOND_API
from db.database import init_db, get_users_to_notify

from handlers.channels import channels_router
from handlers.standart import standart_router
from handlers.bonds import bonds_router

dp.include_router(standart_router)
dp.include_router(channels_router)
dp.include_router(bonds_router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def notify_users(api_url, bot: Bot):
    while True:
        logger.info(f"{datetime.utcnow()} Checking for users...")
        notifications = await get_users_to_notify(api_url)
        if notifications:
            for user_id, bond_index, bonus in notifications:
                await bot.send_message(user_id, f"Бонд {bond_index} достиг бонуса {bonus}.")
        await asyncio.sleep(600)

async def main():
    asyncio.create_task(notify_users(BOND_API, bot))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(init_db())
    asyncio.run(main())