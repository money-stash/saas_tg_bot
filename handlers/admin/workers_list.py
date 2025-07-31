from aiogram.types import Message
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from api.user_api import get_users
from keyboards.inline.user import get_back_to_main_kb
from config import ADMIN_IDS

router = Router()


@router.message(F.text.startswith('/list'))
async def print_workers_list(message: Message, state: FSMContext, bot: Bot, user_id: int):
    if user_id in ADMIN_IDS:
        users = await get_users()

        msg_text = "Список пользователей:\n"
        for user in users["users"]:
            username = user.get('username')
            role = user.get('role')
            status = user.get('status')

            if str(status) == "True":
                status = "активен"
            else:
                status = "заблокирован"

            u_id = user.get('user_id')

            msg_text += f"@{username} | status: {status} | role: {role} | id: {u_id}\n"

        await message.answer(msg_text, reply_markup=await get_back_to_main_kb())


