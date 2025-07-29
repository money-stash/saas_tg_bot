import os
from aiogram.types import (
    CallbackQuery,
    Message,
)
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from states.user import UploadLinkFile
from api.user_api import upload_file_to_link, add_link
from keyboards.inline.user import get_cancel_menu, get_back_to_main_kb


router = Router()


@router.callback_query(F.data.startswith("upload_link_words:"))
async def start_upload_link_words(call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int):
    link_id = call.data.split("upload_link_words:")[1]

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="Отправьте .тхт файл со словами для спама.\nКаждое слово с новой строки.",
        reply_markup=await get_cancel_menu(),
    )

    await state.update_data({"link_id": link_id, 'msg_id': call.message.message_id})
    await state.set_state(UploadLinkFile.link_file)


@router.message(UploadLinkFile.link_file)
async def document_handler(message: Message, bot: Bot, state: FSMContext, user_id: int):
    if document := message.document:
        data = await state.get_data()

        os.makedirs("downloads", exist_ok=True)
        filename = message.document.file_name or "file"
        destination = f"downloads/{filename}"

        file_obj = await bot.get_file(message.document.file_id)
        await bot.download_file(file_obj.file_path, destination)

        await bot.delete_message(message_id = message.message_id, chat_id = user_id)

        answer = await upload_file_to_link(link_id=data['link_id'], file_path=destination)
        if answer['success'] is True:
            await bot.edit_message_text(
                chat_id=user_id,
                message_id=data['msg_id'],
                text="✅ Слова успешно загружены!",
                reply_markup=await get_back_to_main_kb(),
            )
        else:
            await bot.edit_message_text(
                chat_id=user_id,
                message_id=data['msg_id'],
                text="❌ Ошибка при загрузке слов!",
                reply_markup=await get_back_to_main_kb(),
            )

        await state.clear()

        try:
            os.remove(destination)
        except Exception as ex:
            print(f"error while deleting words file: {ex}")
    else:
        await message.reply("Что это за файл?")
