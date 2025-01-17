from settings import CHANNELS, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def check_user_subscription(user_id: int) -> list:
    """
    Проверяет подписку пользователя на заданный список каналов.

    :param user_id: ID пользователя Telegram.
    :return: Список каналов, на которые пользователь не подписан.
    """
    not_subscribed = []

    for channel in CHANNELS:
        try:
            if channel.startswith("https://t.me/") or channel.startswith("@"):
                chat = await bot.get_chat(channel)
                channel_id = chat.id
            else:
                channel_id = int(channel)

            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)

            if member.status not in ['member', 'administrator', 'creator']:
                not_subscribed.append(channel)

        except Exception as e:
            print(f"Ошибка проверки подписки на канал {channel}: {e}")
            not_subscribed.append(channel)

    return not_subscribed


async def create_channels_keyboard(channels: list, include_subscribed_button: bool = False) -> InlineKeyboardMarkup:
    """
    Создаёт клавиатуру для подписки на каналы.

    :param channels: Список каналов.
    :param include_subscribed_button: Добавлять ли кнопку "Я подписался".
    :return: Клавиатура с кнопками для подписки на каналы.
    """
    inline_keyboard = []

    for channel in channels:
        try:
            if channel.startswith("https://t.me/") or channel.startswith("@"):
                chat = await bot.get_chat(channel)
                channel_name = chat.title
                url = f"https://t.me/{chat.username}" if chat.username else None
            else:
                channel_id = int(channel)
                chat = await bot.get_chat(channel_id)
                channel_name = chat.title
                url = f"https://t.me/{chat.username}" if chat.username else None

            if url:
                inline_keyboard.append([InlineKeyboardButton(text=channel_name, url=url)])
            else:
                print(f"Канал {channel_name} не имеет публичного username.")

        except Exception as e:
            print(f"Ошибка добавления кнопки для канала {channel}: {e}")

    if include_subscribed_button:
        inline_keyboard.append([InlineKeyboardButton(text="Я подписался", callback_data="subscribed")])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)



