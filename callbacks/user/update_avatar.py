import json
from aiogram.types import (
    CallbackQuery,
    Message,
    PhotoSize,
)
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

import os

from database.db import db
from states.user import UpdateAvatar
from api.user_api import get_session_info, get_users, upload_avatar
from keyboards.inline.user import get_cancel_menu

router = Router()


@router.callback_query(F.data.startswith("change_image:"))
async def start_update_avatar(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    user_id = call.from_user.id

    all_users = get_users()
    if db.user_exists(all_users, user_id):
        session_id = call.data.split(":", 1)[1]

        await state.update_data({"session_id": session_id})
        await state.set_state(UpdateAvatar.avatar)
        await bot.edit_message_text(
            text="📸 Отправьте новое изображение для сессии",
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            reply_markup=await get_cancel_menu(),
        )


@router.message(F.photo)
async def receive_avatar(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    photo: PhotoSize = message.photo[-1]
    file_id = photo.file_id

    file = await bot.get_file(file_id)
    path = file.file_path
    os.makedirs("images", exist_ok=True)
    destination = os.path.join("images", f"{file_id}.jpg")

    await bot.download_file(path, destination)

    response = upload_avatar(
        session_id=data.get("session_id"),
        avatar_path=destination,
    )

    try:
        os.remove(destination)
    except:
        pass

    await message.answer(f"Файл загружен: {response}")
