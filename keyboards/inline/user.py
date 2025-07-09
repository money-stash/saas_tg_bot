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
