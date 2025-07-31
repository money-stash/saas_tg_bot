from aiogram.types import Message
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from api.user_api import ban_user_bot
from keyboards.inline.user import get_back_to_main_kb
from config import ADMIN_IDS

router = Router()


@router.message(F.text.startswith('/ban'))
async def start_ban_user(message: Message, state: FSMContext, bot: Bot, user_id: int):
    if user_id in ADMIN_IDS:
        username = message.text.split(" ")[1]

        is_banned = await ban_user_bot(username)

        if is_banned['status'] == 'ok':
            await message.answer('Пользователь заблокирован', reply_markup=await get_back_to_main_kb())
        else:
            await message.answer('Пользователь не заблокирован', reply_markup=await get_back_to_main_kb())
