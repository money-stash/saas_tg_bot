import json

from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from api.user_api import get_users, get_sessions_info

router = Router()


@router.callback_query(F.data.startswith("open_privacy:"))
async def open_privacy(
    callback: CallbackQuery,
    state: FSMContext,
    bot: Bot,
):
    session_id = callback.data.split(":")[1]
    user_id = callback.from_user.id

    # api_answer = await open_session_privacy(session_id)

    sessions_info = await get_sessions_info()

    kb = []

    kb.append(
        [
            InlineKeyboardButton(
                text="⏫️ Загрузить сессию", callback_data="upload_sessions"
            )
        ]
    )

    for session in sessions_info.get("sessions", []):
        kb.append(
            [
                InlineKeyboardButton(
                    text=f"Сессия {session['id']}",
                    callback_data=f"session_info:{session['id']}",
                )
            ]
        )

    kb.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")])

    if api_answer.get("success"):
        msg_text = "👥 Приватность сессии открыта"
    else:
        msg_text = "❌ Ошибка при открытии приватности сессии"

    await callback.message.edit_text(
        text=msg_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb),
    )
