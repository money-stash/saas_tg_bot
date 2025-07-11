from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from database.db import db
from states.user import Login
from api.user_api import get_users, get_sessions_info
from keyboards.inline.user import get_sessions_kb

router = Router()


@router.callback_query(F.data == "sessions_menu")
async def get_sessions_menu(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    user_id = call.from_user.id

    all_users = get_users()
    if db.user_exists(all_users, user_id):
        sessions_info = get_sessions_info()
        sessions_count = len(sessions_info.get("sessions", []))

        kb = []

        for session in sessions_info.get("sessions", []):
            kb.append(
                InlineKeyboardButton(
                    text=f"Сессия {session['id']}",
                    callback_data=f"session_info:{session['id']}",
                )
            )
        kb.append(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))

        await call.message.edit_text(
            text=f"👥 Вы открыли меню сессий\n\nВ общем: <b>{sessions_count}</b> сессий",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[kb]),
        )
    else:
        await call.message.edit_text(
            text="✏️ Напишите ваш ключ доступ для регистрации",
        )
        await state.set_state(Login.login_key)
