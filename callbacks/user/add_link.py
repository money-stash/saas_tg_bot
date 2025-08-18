import json
from aiogram.types import (
    CallbackQuery,
    Message,
)
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from states.user import AddLink
from api.user_api import check_link, add_link
from keyboards.inline.user import get_cancel_menu, get_back_to_main_kb, get_suc_add_link


router = Router()


@router.callback_query(F.data == "add_link")
async def add_link_route(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="Введите ЮЗЕРНЕЙМ канала, без @, например: channel_username:",
        reply_markup=await get_cancel_menu(),
    )
    await state.update_data({"msg_id": call.message.message_id})
    await state.set_state(AddLink.link)


@router.message(AddLink.link)
async def end_add_link(message: Message, state: FSMContext, bot: Bot, user_id: int):
    if message.text:
        data = await state.get_data()
        link = message.text

        await bot.delete_message(chat_id=user_id, message_id=message.message_id)

        is_link_valid = await check_link(link)
        if is_link_valid.get("exists")[0] is True:
            await add_link(link, link_name=is_link_valid.get("exists")[1])
            await state.update_data({"link": link})
            await bot.edit_message_text(
                chat_id=user_id,
                message_id=data["msg_id"],
                text="✅ Канал успешно добавлен!\n📄 Загрузите тхт со словами",
                reply_markup=await get_suc_add_link(),
            )

        else:
            await bot.edit_message_text(
                chat_id=user_id,
                message_id=data["msg_id"],
                text="❌ Канал не найден. Пожалуйста, введите корректную ссылку.",
                reply_markup=await get_cancel_menu(),
            )

        await state.clear()
