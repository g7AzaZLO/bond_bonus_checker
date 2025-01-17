from aiogram import Router, types

from utils.channel import create_channels_keyboard, check_user_subscription

channels_router = Router()

@channels_router.callback_query(lambda callback_query: callback_query.data == "subscribed")
async def handle_subscribed_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    not_subscribed = await check_user_subscription(user_id)

    if not_subscribed:
        keyboard = await create_channels_keyboard(
            not_subscribed,
            include_subscribed_button=True
        )
        await callback_query.message.answer("Вы все еще не подписались на каналы:", reply_markup=keyboard)
    else:
        await callback_query.message.answer(f"Вы подписаны", parse_mode="MARKDOWN")
