import os
from aiogram.types import CallbackQuery, Message
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from database.db import db
from states.user import UploadSession, Login
from api.user_api import get_users, get_sessions_info, upload_session_files
from keyboards.inline.user import get_back_to_main_kb, get_cancel_menu

router = Router()


@router.callback_query(F.data == "upload_sessions")
async def get_upload_session(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    user_id = call.from_user.id

    all_users = await get_users()
    if db.user_exists(all_users, user_id):
        await call.message.edit_text(
            text="Отправьте файл сессии в формате .session",
            reply_markup=await get_cancel_menu(),
        )
        await state.set_state(UploadSession.session_file)
        await state.update_data({"msg_id": call.message.message_id})

    else:
        await call.message.edit_text(
            text="✏️ Напишите ваш ключ доступ для регистрации",
        )
        await state.set_state(Login.login_key)


@router.message(UploadSession.session_file)
async def upload_session_file(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id

    if message.document and message.document.file_name.endswith(".session"):
        data = await state.get_data()
        downloaded = await bot.download(
            message.document, destination=f"downloads/{user_id}.session"
        )
        await state.update_data(session_file=f"downloads/{user_id}.session")

        await bot.delete_message(chat_id=user_id, message_id=message.message_id)

        await bot.edit_message_text(
            chat_id=user_id,
            message_id=data["msg_id"],
            text="Отправьте файл сессии в формате .json",
            reply_markup=await get_cancel_menu(),
        )
        await state.set_state(UploadSession.json_file)

    else:
        await bot.delete_message(chat_id=user_id, message_id=message.message_id)


@router.message(UploadSession.json_file)
async def upload_json_file(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id

    if message.document and message.document.file_name.endswith(".json"):
        data = await state.get_data()
        downloaded = await bot.download(
            message.document, destination=f"downloads/{user_id}.json"
        )

        await bot.delete_message(chat_id=user_id, message_id=message.message_id)
        await bot.delete_message(chat_id=user_id, message_id=data["msg_id"])

        session_file_path = data["session_file"]
        json_file_path = f"downloads/{user_id}.json"

        upload_response = await upload_session_files(session_file_path, json_file_path)

        if upload_response.get("success") == True:
            await bot.send_message(
                chat_id=user_id,
                text=f"✅ Сессия успешно загружена!",
                reply_markup=await get_back_to_main_kb(),
            )
        else:
            await bot.send_message(
                chat_id=user_id,
                text=f"❌ Ошибка при загрузке сессии!",
                reply_markup=await get_back_to_main_kb(),
            )

        await state.clear()

        try:
            os.remove(session_file_path)
            os.remove(json_file_path)
        except:
            pass

    else:
        await bot.delete_message(chat_id=user_id, message_id=message.message_id)
