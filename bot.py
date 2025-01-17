from handlers.channels import channels_router
from settings import dp, bot
from handlers.standart import standart_router


dp.include_router(standart_router)
dp.include_router(channels_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
