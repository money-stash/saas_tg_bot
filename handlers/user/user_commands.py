from aiogram import Router, F, Bot
from aiogram.types import Message

from database.db import db
from api.user_api import get_users

router = Router()


@router.message(F.text == "/start")
async def start_func(msg: Message, bot: Bot, user_id: int):
    first_name = msg.from_user.first_name
    username = msg.from_user.username

    all_users = get_users()
    print(all_users)
    is_user = db.user_exists(all_users, user_id)

    print(is_user)
