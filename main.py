import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from middlewares.user_info import UserInfoMiddleware

from handlers.user import user_commands, login
from callbacks.user import back_to_main, open_sessions_menu

from config import TOKEN


async def main():
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.message.outer_middleware(UserInfoMiddleware())
    dp.callback_query.outer_middleware(UserInfoMiddleware())

    dp.include_routers(
        user_commands.router,
        login.router,
        back_to_main.router,
        open_sessions_menu.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
