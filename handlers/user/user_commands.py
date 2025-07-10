from aiogram.types import Message
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from database.db import db
from states.user import Login, UpdateLogin
from api.user_api import get_users
from keyboards.inline.user import get_main_kb

router = Router()


@router.message(F.text == "/start")
async def start_func(msg: Message, bot: Bot, state: FSMContext, user_id: int):
    first_name = msg.from_user.first_name
    all_users = get_users()
    print(all_users)

    is_user = db.user_exists(all_users, user_id)

    if is_user:
        for user in all_users["users"]:
            if user["user_id"] == int(user_id):
                user_data = user

        if user_data["status"] == False:
            await msg.answer("❌ Вы заблокированы!")
            return

        if user_data["key_id"] == 0:
            await msg.answer("✏️ Напишите ваш ключ доступ для регирстрации")
            await state.set_state(UpdateLogin.login_key)
            return

        await msg.answer(
            f"👋 Добрый день, <b>{first_name}</b>", reply_markup=await get_main_kb()
        )
    else:
        await msg.answer("✏️ Напишите ваш ключ доступ для регирстрации")
        await state.set_state(Login.login_key)
