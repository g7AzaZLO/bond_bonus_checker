from aiogram import Router, types
from aiogram.filters import Command

from utils.channel import check_user_subscription, create_channels_keyboard

standart_router = Router()

@standart_router.message(Command("start"))
async def start_command(message: types.Message):
    user_id = message.from_user.id

    not_subscribed = await check_user_subscription(user_id)

    if not_subscribed:
        keyboard = await create_channels_keyboard(
            not_subscribed,
            include_subscribed_button=True
        )
        await message.answer("Подпишитесь на каналы ниже, чтобы получить доступ:", reply_markup=keyboard)
    else:
        await message.answer(f"Используйте: /setbond <индекс бонда> <процент бонуса>\n\nС 1 аккаунта можно подписться только на 1 уведомление. Если вы прописали сначала один бонд на один процент, потом еще раз прописали команду с другими значениями, то присылать уведомление он будет по последнему\n\nБот проверяет бонды каждые 5 минут. Если бонус вашего бонда выше введенного вами значения, то вам придет уведомление",parse_mode="MARKDOWN")

@standart_router.message(Command("help"))
async def help_command(message: types.Message):
    help_text = """
Доступные команды:

1. **/start** — Проверка подписки на канал и доступ к функционалу бота.
2. **/setbond <индекс> <цель>** — Установить уведомление на бонд.
   - Пример: `/setbond 2015 5.5`
3. **/listbonds** — Вывести список всех ваших активных уведомлений.
4. **/deletebond <индекс>** — Удалить уведомление на бонд.
   - Пример: `/deletebond 2015`
5. **/allbonds** — Список всех доступных бондов.
6. **/help** — Вывести это сообщение.

Бот проверяет бонды каждые 5 минут. Уведомления отправляются только если бонус бонда соответствует вашим условиям.
"""
    await message.reply(help_text, parse_mode="MARKDOWN")
