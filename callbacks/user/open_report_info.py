from aiogram.types import (
    CallbackQuery,
)
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from database.db import db
from states.user import ChangeName
from api.user_api import get_report_info
from keyboards.inline.user import get_cancel_menu, get_report_info_kb

router = Router()


@router.callback_query(F.data.startswith("open_report_"))
async def print_repo_info(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    repo_id = call.data.split("open_report_")[-1]
    info = await get_report_info(repo_id)

    msg_text = f"ID задачи: <b>{info['id']}</b>\n\n"
    msg_text += f"Тип задачи: <b>{info['type']}</b>\n"
    msg_text += f"ID пользователя(создателя): <b>{info['worker_id']}</b>\n"
    msg_text += f"Дата и время создания: <b>{info['date']}</b>"

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=msg_text,
        reply_markup=await get_report_info_kb(info["id"]),
    )
