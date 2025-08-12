import json

from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from database.db import db
from states.user import Login
from api.user_api import get_users, get_session_info
from keyboards.inline.user import get_back_to_main_kb

router = Router()


def build_session_keyboard(session_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="🌌 Изменить изображение",
                callback_data=f"change_image:{session_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="✏️ Изменить имя", callback_data=f"change_name:{session_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="✏️ Изменить фамилию", callback_data=f"change_surname:{session_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="✏️ Изменить username",
                callback_data=f"change_username:{session_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="✏️ Изменить bio",
                callback_data=f"change_bio:{session_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔐 Конфиденциальность",
                callback_data=f"privacy_settings:{session_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🗑️ Удалить сессию", callback_data=f"delete_session:{session_id}"
            ),
        ],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="sessions_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def build_privacy_keyboard(
    privacy_data: dict, session_id: int
) -> InlineKeyboardMarkup:
    label_map = {
        "phone_number": "Номер телефона",
        "last_seen": "Время захода",
        "profile_photo": "Фотографии профиля",
        "message_forwards": "Пересылка сообщений",
        "calls": "Звонки",
        "voice_messages": "Голосовые сообщения",
        "messages": "Сообщения",
        "chat_invites": "Приглашения",
    }
    buttons = []
    for key, value in privacy_data.items():
        if key not in label_map:
            continue
        action = "Скрыть" if value else "Открыть"
        text = f"{action} {label_map[key]}"
        callback_dataa = (
            f"hide:{key}:{session_id}"
            if action == "Скрыть"
            else f"show:{key}:{session_id}"
        )
        buttons.append([InlineKeyboardButton(text=text, callback_data=callback_dataa)])
    buttons.append(
        [
            InlineKeyboardButton(
                text="🔙 Назад", callback_data=f"back_to_session:{session_id}"
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_session_text(session_info: dict) -> str:
    msg_text = "ℹ️ Информация о сессии\n\n"
    msg_text += f"🆔 аккаунта сессии: {session_info['account_id']}\n"
    msg_text += (
        f"📛 Полное имя: {session_info['first_name']} {session_info['last_name']}\n"
    )
    if session_info["username"]:
        msg_text += f"🫆 Имя пользователя: @{session_info['username']}\n"
    else:
        msg_text += "❌ Имя пользователя: не указано\n"
    if session_info["is_valid"]:
        msg_text += "✅ Сессия валидна\n"
    else:
        msg_text += "❌ Сессия невалидна\n"
    msg_text += f"👤 BIO: {session_info['bio']}\n"
    msg_text += "\n\n🔐 Конфиденциальность(True - видят все, False - никто не видит или только контакты)\n"
    msg_text += f"Инвайты в чаты: {session_info['chat_invites']}\n"
    msg_text += f"Пересылка сообщений: {session_info['message_forwards']}\n"
    msg_text += f"Звонки: {session_info['calls']}\n"
    msg_text += f"Номер телефона: {session_info['phone_number']}\n"
    msg_text += f"Фото профиля: {session_info['profile_photo']}\n"
    msg_text += f"Время захода: {session_info['last_seen']}\n"
    return msg_text


@router.callback_query(F.data.startswith("session_info:"))
async def get_session_info_hndlr(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    user_id = call.from_user.id
    all_users = await get_users()
    if db.user_exists(all_users, user_id):
        session_id = call.data.split(":")[1]
        session_data = await get_session_info(session_id)
        session_info = json.loads(session_data)["session"]
        if session_info == "error":
            await call.message.edit_text(
                "Сессия была удалена, так как она невалидна.",
                reply_markup=await get_back_to_main_kb(),
            )
            return
        msg_text = build_session_text(session_info)
        keyboard = build_session_keyboard(session_id=int(session_id))
        await call.message.edit_text(text=msg_text, reply_markup=keyboard)
    else:
        await call.message.edit_text(text="✏️ Напишите ваш ключ доступ для регистрации")
        await state.set_state(Login.login_key)


@router.callback_query(F.data.startswith("privacy_settings:"))
async def open_privacy_settings(call: CallbackQuery, bot: Bot, state: FSMContext):
    session_id = call.data.split(":")[1]
    session_data = await get_session_info(session_id)
    session_info = json.loads(session_data)["session"]
    if session_info == "error":
        await call.message.edit_text(
            "Сессия была удалена, так как она невалидна.",
            reply_markup=await get_back_to_main_kb(),
        )
        return
    keyboard = await build_privacy_keyboard(session_info, session_id=int(session_id))
    await call.message.edit_text(
        text="🔐 Настройки конфиденциальности", reply_markup=keyboard
    )


@router.callback_query(F.data.startswith("back_to_session:"))
async def back_to_session(call: CallbackQuery, bot: Bot, state: FSMContext):
    session_id = call.data.split(":")[1]
    session_data = await get_session_info(session_id)
    session_info = json.loads(session_data)["session"]
    if session_info == "error":
        await call.message.edit_text(
            "Сессия была удалена, так как она невалидна.",
            reply_markup=await get_back_to_main_kb(),
        )
        return
    msg_text = build_session_text(session_info)
    keyboard = build_session_keyboard(session_id=int(session_id))
    await call.message.edit_text(text=msg_text, reply_markup=keyboard)
