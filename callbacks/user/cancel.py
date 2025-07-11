from aiogram.types import CallbackQuery, Message
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from database.db import db
from states.user import UploadSession, Login
from api.user_api import get_users, get_sessions_info
from keyboards.inline.user import get_main_kb

router = Router()


@router.callback_query(F.data == "cancel")
async def cancel_action(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    user_id = call.from_user.id

    await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)

    await bot.send_message(
        chat_id=user_id,
        text="❌ Действие отменено. Вы вернулись в главное меню.",
        reply_markup=await get_main_kb(),
    )
