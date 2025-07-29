from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram import Router, F, Bot

from api.user_api import get_link
from keyboards.inline.user import get_link_info_kb

router = Router()


@router.callback_query(F.data.startswith("open_link"))
async def open_link_info(call: CallbackQuery, bot: Bot, user_id: int):
    link_id = call.data.split("open_link_")[-1]
    link_info = await get_link(link_id=int(link_id))

    msg_text = f"🆔 ID канала: {link_info['id']}\n📜 Название канала: {link_info['link_name']}\n\n🔗 Ссылка: @{link_info['link']}"
    if link_info['spam_text'] == "False":
        msg_text += f"\n📄 Текста для спама - нет!"
    else:
        msg_text += f"\n📄 Текст для спама: {link_info['spam_text']}"

    await bot.edit_message_text(
        text=str(msg_text),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=await get_link_info_kb(link_id, is_active=link_info['active'])
    )
