from aiogram.types import Message
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from database.db import db
from states.user import UpdateLogin
from keyboards.inline.user import get_main_kb
from api.user_api import get_key_info, update_add_new_user

router = Router()


@router.message(UpdateLogin.login_key)
async def update_start_func(msg: Message, bot: Bot, state: FSMContext, user_id: int):
    username = msg.from_user.username

    key = msg.text

    key_info = get_key_info(key)

    if key_info["key_info"] == False:
        await msg.answer("❌ Такого ключа не существует!")
    else:
        key_data = key_info["key_info"]
        if int(key_data["user_id"]) != 0:
            await msg.answer("⁉️ Этот ключ уже используется!")
        else:
            update_add_new_user(user_id, username, key)

            await msg.answer(
                "🥳 Вы успешно зарегестрировались", reply_markup=await get_main_kb()
            )

            await state.clear()
