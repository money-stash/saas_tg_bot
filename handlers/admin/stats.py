from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from api.user_api import get_all_reports
from config import ADMIN_IDS

router = Router()


@router.message(F.text.startswith('/stats'))
async def start_create_new_token(message: Message, state: FSMContext, bot: Bot, user_id: int):
    if user_id in ADMIN_IDS:
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

        await bot.send_message(
            chat_id=user_id,
            text="Выберите отчет",
            reply_markup=keyboard,
        )