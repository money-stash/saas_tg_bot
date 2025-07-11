from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from database.db import db
from states.user import Login
from api.user_api import get_users, get_session_info
from keyboards.inline.user import get_sessions_info_kb, get_back_to_main_kb

router = Router()


@router.callback_query(F.data.startswith("session_info:"))
async def get_session_info_hndlr(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    user_id = call.from_user.id

    all_users = get_users()

    if db.user_exists(all_users, user_id):
        session_id = call.data.split(":")[1]
        session_info = get_session_info(session_id)
        if session_info:
            await call.message.edit_text(
                text=f"Информация о сессии {session_id}:\n{session_info}",
                reply_markup=await get_sessions_info_kb(session_id),
            )
        else:
            await call.message.edit_text(
                text=f"Сессия {session_id} не найдена.",
                reply_markup=await get_back_to_main_kb(),
            )
    else:
        await call.message.edit_text(
            text="✏️ Напишите ваш ключ доступ для регистрации",
        )
        await state.set_state(Login.login_key)
