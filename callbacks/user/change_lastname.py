import json
from aiogram.types import (
    CallbackQuery,
    Message,
)
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from database.db import db
from states.user import ChangeSurname
from api.user_api import get_session_info, get_users, update_surname
from keyboards.inline.user import get_cancel_menu, get_back_to_session

router = Router()


@router.callback_query(F.data.startswith("change_surname:"))
async def start_update_surname(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await state.set_state(ChangeSurname.surname)

    await bot.edit_message_text(
        text="✏️ Введите новое фамилию для сессии:\n\nЧТОБЫ УБРАТЬ ФАМИЛИЮ напишите: <i>None</i> или <i>none</i>",
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=await get_cancel_menu(),
    )

    await state.update_data(
        {"msg_id": call.message.message_id, "session_id": call.data.split(":")[1]}
    )


@router.message(F.text, ChangeSurname.surname)
async def update_surname_hndlr(msg: Message, bot: Bot, state: FSMContext):
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

        session_info["surname"] = new_name
        is_updated = await update_surname(session_id, new_name)

        if is_updated["success"] is False:
            msg_text = "❌ Ошибка при обновлении фамилии сессии. Попробуйте позже."
        else:
            msg_text = f"✅ Фамилия сессии успешно обновлена на: {new_name}"

        await bot.edit_message_text(
            text=msg_text,
            chat_id=user_id,
            message_id=data["msg_id"],
            reply_markup=await get_back_to_session(session_id),
        )

    else:
        await msg.answer("✏️ Напишите ваш ключ доступ для регистрации")
        await state.set_state(ChangeSurname.name)
