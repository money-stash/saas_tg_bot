import json
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram import Router, F, Bot
from api.user_api import get_all_links

router = Router()


@router.callback_query(F.data == "links_menu")
async def open_links_menu(call: CallbackQuery, bot: Bot, user_id: int):
    links = await get_all_links()
    print(links)
    links_json = links['links']

    kb = []

    for link in links_json:
        kb.append(
            [
                InlineKeyboardButton(
                    text=link["link_name"],
                    callback_data=f'open_link_{link["id"]}',
                )
            ]
        )
    kb.append(
        [InlineKeyboardButton(text="➕ Добавить канал", callback_data="add_link")]
    )
    kb.append(
        [InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_main")]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await bot.edit_message_text(
        text="🔗 Список доступных ссылок:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=keyboard,
    )
