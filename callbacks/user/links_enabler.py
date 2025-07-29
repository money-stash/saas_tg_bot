from aiogram.types import (
    CallbackQuery,
)
from aiogram import Router, F, Bot

from api.user_api import get_link, update_status
from keyboards.inline.user import get_back_to_main_kb

router = Router()


@router.callback_query(F.data.startswith("disable_link:"))
async def start_disable_link(call: CallbackQuery, bot: Bot, user_id: int):
    link_id = call.data.split("disable_link:")[-1]
    link_info = await get_link(link_id=int(link_id))

    await update_status(int(link_id), False)

    await bot.edit_message_text(
        text=f"✅Канал {link_info['link_name']} отключен.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=await get_back_to_main_kb()
    )


@router.callback_query(F.data.startswith("enable_link:"))
async def start_enable_link(call: CallbackQuery, bot: Bot, user_id: int):
    link_id = call.data.split("enable_link:")[-1]
    link_info = await get_link(link_id=int(link_id))

    await update_status(int(link_id), True)

    await bot.edit_message_text(
        text=f"✅Канал {link_info['link_name']} включен.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=await get_back_to_main_kb()
    )
