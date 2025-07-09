from aiogram.types import CallbackQuery
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from database.db import db
from states.user import Login
from api.user_api import get_users
from keyboards.inline.user import get_sessions_kb

router = Router()


@router.callback_query(F.data == "sessions_menu")
async def get_sessions_menu(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    await state.clear()
    all_users = get_users()

    is_user = db.user_exists(all_users, user_id)

    if is_user:
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=f"👥 Вы открыли меню сессий\n\nВ общем: <b>0</b> сессий",
            reply_markup=await get_sessions_kb(),
        )
    else:
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=f"✏️ Напишите ваш ключ доступ для регирстрации",
        )
        await state.set_state(Login.login_key)
