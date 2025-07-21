import os
from random import randint

from aiogram.types import CallbackQuery, FSInputFile
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from api.user_api import download_report_file, get_report_info
from keyboards.inline.user import get_cancel_menu, get_report_info_kb

router = Router()


@router.callback_query(F.data.startswith("download_report_"))
async def start_download_report(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    repo_info = await get_report_info(report_id=call.data.split("download_report_")[-1])
    download_file = await download_report_file(
        path=repo_info["path"], save_as=f"reports/{randint(1000000,10000000)}.csv"
    )

    if download_file:
        file = FSInputFile(download_file)

        await bot.send_document(chat_id=user_id, document=file)

        try:
            os.remove(download_file)
        except:
            pass
