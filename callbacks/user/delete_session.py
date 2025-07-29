from aiogram.types import CallbackQuery
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from keyboards.inline.user import get_back_to_main_kb
from api.user_api import delete_session_api

router = Router()


@router.callback_query(F.data.startswith("delete_session:"))
async def del_session(call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int):
    session_id = call.data.split(":")[-1]
    print(session_id)

    await delete_session_api(session_id)

    msg_text = f"✅ Сессия {session_id} успешно удалена."

    await bot.edit_message_text(
        text=msg_text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=await get_back_to_main_kb(),
    )
