import json
from aiogram.types import (
    CallbackQuery,
    Message,
)
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from database.db import db
from states.user import ChangeName
from api.user_api import get_session_info, get_users, update_first_name
from keyboards.inline.user import get_cancel_menu, get_back_to_main_kb

router = Router()


@router.callback_query(F.data.startswith("change_name:"))
async def start_update_name(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await state.set_state(ChangeName.name)

    await bot.edit_message_text(
        text="✏️ Введите новое имя для сессии:",
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=await get_cancel_menu(),
    )

    await state.update_data(
        {"msg_id": call.message.message_id, "session_id": call.data.split(":")[1]}
    )


@router.message(F.text, ChangeName.name)
async def update_name_hndlr(msg: Message, bot: Bot, state: FSMContext):
    user_id = msg.from_user.id
    all_users = await get_users()

    if db.user_exists(all_users, user_id):
        data = await state.get_data()
        session_id = data["session_id"]
        new_name = msg.text.strip()

        session_data = await get_session_info(session_id)
        session_info = json.loads(session_data)["session"]

        if not new_name:
            await msg.answer("❌ Имя не может быть пустым. Попробуйте снова.")
            return

        await bot.delete_message(
            chat_id=user_id,
            message_id=msg.message_id,
        )

        session_info["first_name"] = new_name
        is_updated = await update_first_name(session_id, new_name)

        if is_updated["success"] is False:
            msg_text = "❌ Ошибка при обновлении имени сессии. Попробуйте позже."
        else:
            msg_text = f"✅ Имя сессии успешно обновлено на: {new_name}"

        await bot.edit_message_text(
            text=msg_text,
            chat_id=user_id,
            message_id=data["msg_id"],
            reply_markup=await get_back_to_main_kb(),
        )

    else:
        await msg.answer("✏️ Напишите ваш ключ доступ для регистрации")
        await state.set_state(ChangeName.name)
