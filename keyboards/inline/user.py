from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_main_kb():
    kb = [
        [InlineKeyboardButton(text="👥 Сессии", callback_data="sessions_menu")],
        [InlineKeyboardButton(text="🔗 Ссылки", callback_data="links_menu")],
        [InlineKeyboardButton(text="🚀 Запуск", callback_data="launch_menu")],
        [InlineKeyboardButton(text="📈 Отчёты", callback_data="report_menu")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def get_sessions_kb():
    kb = [
        [
            InlineKeyboardButton(
                text="⏫️ Загрузить сессию", callback_data="upload_sessions"
            )
        ],
        [InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_main")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def get_sessions_info_kb(session_id, conf):
    kb = [
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
    ]

    if conf:
        kb.append(
            [
                InlineKeyboardButton(
                    text="Закрыть приватность",
                    callback_data=f"close_privacy:{session_id}",
                ),
            ],
        )
    else:
        kb.append(
            [
                InlineKeyboardButton(
                    text="Открыть приватность",
                    callback_data=f"open_privacy:{session_id}",
                ),
            ],
        )

    kb.append(
        [
            InlineKeyboardButton(
                text="🗑️ Удалить сессию", callback_data=f"delete_session:{session_id}"
            ),
        ]
    )
    kb.append(
        [InlineKeyboardButton(text="🔙 Назад", callback_data="sessions_menu")],
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def get_back_to_main_kb():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
        ]
    )
    return kb


async def get_cancel_menu():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
        ]
    )
    return kb
