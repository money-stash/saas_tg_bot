from aiogram.types import CallbackQuery
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from database.db import db
from states.user import Login
from api.user_api import get_users
from keyboards.inline.user import get_main_kb

router = Router()


@router.callback_query(F.data == "back_to_main")
async def get_back_to_main(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    await state.clear()
    first_name = call.from_user.first_name
    all_users = await get_users()

    is_user = db.user_exists(all_users, user_id)

    if is_user:
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=f"👋 Добрый день, <b>{first_name}</b>",
            reply_markup=await get_main_kb(),
        )
    else:
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=f"✏️ Напишите ваш ключ доступ для регирстрации",
        )
        await state.set_state(Login.login_key)
