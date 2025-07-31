from aiogram.types import Message
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from states.admin import GetNewToken
from api.user_api import create_token_bot
from keyboards.inline.user import get_back_to_main_kb
from config import ADMIN_IDS

router = Router()


@router.message(F.text.startswith('/get_token'))
async def start_create_new_token(message: Message, state: FSMContext, bot: Bot, user_id: int):
    if user_id in ADMIN_IDS:
        await message.answer("Введите название для нового токена")
        await state.set_state(GetNewToken.token_name)


@router.message(GetNewToken.token_name)
async def get_token_name(message: Message, state: FSMContext, bot: Bot, user_id: int):
    token_name = message.text
    await state.update_data(token_name=token_name)

    created_token = await create_token_bot(token_name)

    await message.answer(f"Токен: {created_token['token']}", reply_markup=await get_back_to_main_kb())

    await state.clear()


