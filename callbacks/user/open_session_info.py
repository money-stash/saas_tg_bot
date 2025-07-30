import json

from aiogram.types import CallbackQuery
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

    all_users = await get_users()

    if db.user_exists(all_users, user_id):
        session_id = call.data.split(":")[1]
        session_data = await get_session_info(session_id)
        session_info = json.loads(session_data)["session"]

        msg_text = "ℹ️ Информация о сессии\n\n"
        msg_text += f"🆔 аккаунта сессии: {session_info['account_id']}\n"
        msg_text += (
            f"📛 Полное имя: {session_info['first_name']} {session_info['last_name']}\n"
        )
        if session_info["username"]:
            msg_text += f"🫆 Имя пользователя: @{session_info['username']}\n"
        else:
            msg_text += "❌ Имя пользователя: не указано\n"

        if session_info["is_valid"]:
            msg_text += "✅ Сессия валидна\n"
        else:
            msg_text += "❌ Сессия невалидна\n"

        msg_text += f"👤 BIO: {session_info['bio']}\n"

        if session_info:
            await call.message.edit_text(
                text=msg_text,
                reply_markup=await get_sessions_info_kb(
                    session_id, conf=session_info["is_private"]
                ),
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
