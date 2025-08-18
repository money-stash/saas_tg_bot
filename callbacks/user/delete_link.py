from aiogram.types import CallbackQuery
from aiogram import Router, F, Bot

from api.user_api import delete_link_request
from keyboards.inline.user import get_suc_add_link

router = Router()


@router.callback_query(F.data.startswith("delete_link:"))
async def delete_link_info(call: CallbackQuery, bot: Bot, user_id: int):
    link_id = call.data.split("delete_link:")[-1]

    await delete_link_request(link_id=int(link_id))

    await bot.edit_message_text(
        text="🔗 Ссылка успешно удалена.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=await get_suc_add_link(),
    )
