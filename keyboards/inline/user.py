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


async def get_newtask_types_menu():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Спам", callback_data="new_task_spam")],
            [InlineKeyboardButton(text="Парсинг", callback_data="new_task_parse")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
        ]
    )
    return kb


async def get_report_info_kb(report_id):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬇️ Скачать отчёт", callback_data=f"download_report_{report_id}"
                )
            ],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")],
        ]
    )
    return kb

async def get_link_info_kb(link_id, is_active):
    kb = []
    kb.append([InlineKeyboardButton(text="⏫Загрузить/обновить слова", callback_data=f"upload_link_words:{link_id}")])

    if is_active:
        kb.append([InlineKeyboardButton(text="⏸️Отключить ссылку", callback_data=f"disable_link:{link_id}")])
    else:
        kb.append([InlineKeyboardButton(text="▶️ Включить ссылку", callback_data=f"enable_link:{link_id}")])

    kb.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")],)
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    return keyboard
