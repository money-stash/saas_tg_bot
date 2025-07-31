import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from middlewares.user_info import UserInfoMiddleware

from handlers.user import user_commands, login, update_login
from handlers.admin import get_token, workers_list, stats, ban_user
from callbacks.user import (
    back_to_main,
    open_sessions_menu,
    open_session_info,
    upload_sessions,
    cancel,
    open_privacy,
    update_avatar,
    change_name,
    change_lastname,
    change_username,
    launch_task,
    report_menu,
    open_report_info,
    download_report,
    open_links_menu,
    delete_session,
    add_link,
    open_link,
    upload_link_words,
    links_enabler,
    change_bio_hndlr,
    hide_action,
    open_action
)

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
        update_login.router,
        open_session_info.router,
        upload_sessions.router,
        cancel.router,
        open_privacy.router,
        update_avatar.router,
        change_name.router,
        change_lastname.router,
        change_username.router,
        launch_task.router,
        report_menu.router,
        open_report_info.router,
        download_report.router,
        open_links_menu.router,
        delete_session.router,
        add_link.router,
        open_link.router,
        upload_link_words.router,
        links_enabler.router,
        change_bio_hndlr.router,
        get_token.router,
        workers_list.router,
        stats.router,
        ban_user.router,
        hide_action.router,
        open_action.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
