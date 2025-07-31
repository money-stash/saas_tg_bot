from aiogram.types import CallbackQuery
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from api.user_api import open_session_privacy
from keyboards.inline.user import get_back_to_session

router = Router()


@router.callback_query(F.data.startswith("show:"))
async def show_action_hndlr(call: CallbackQuery, bot: Bot, state: FSMContext):
    session_id = call.data.split(":")[-1]
    action = call.data.split(":")[1]

    await open_session_privacy(session_id, action)

    await bot.edit_message_text(
        text="✅ Действие выполнено",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=await get_back_to_session(session_id),
    )