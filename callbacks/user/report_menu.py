from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from api.user_api import get_all_reports

router = Router()


@router.callback_query(F.data == "report_menu")
async def print_all_reporst(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    all_reports = await get_all_reports()

    kb = []
    for report in all_reports:
        kb.append(
            [
                InlineKeyboardButton(
                    text=f"{report['date']}",
                    callback_data=f"open_report_{report['id']}",
                )
            ]
        )

    kb.append(
        [InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_main")]
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="Выберите отчет",
        reply_markup=keyboard,
    )
