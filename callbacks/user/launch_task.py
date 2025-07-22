import json
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from database.db import db
from states.user import CreateNewTask
from api.user_api import (
    create_parse_task,
    get_all_reports,
    get_report_info,
    create_spam_task,
)
from keyboards.inline.user import (
    get_newtask_types_menu,
    get_back_to_main_kb,
    get_cancel_menu,
)

router = Router()


@router.callback_query(F.data == "launch_menu")
async def start_add_task(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    await bot.edit_message_text(
        text="Выберите действие:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=await get_newtask_types_menu(),
    )

    await state.set_state(CreateNewTask.task_type)


@router.callback_query(F.data.startswith("new_task_"))
async def choose_task_type(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    task_type = call.data.split("new_task_")[-1]
    await state.update_data({"task_type": task_type})

    await state.update_data({"msg_id": call.message.message_id})

    if task_type == "parse":
        await bot.edit_message_text(
            text="Введите идентификатор группы для запуска задачи:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=await get_cancel_menu(),
        )
        await state.set_state(CreateNewTask.group_identifier)

    elif task_type == "spam":
        all_reports = await get_all_reports()

        kb = []

        for report in all_reports:
            kb.append(
                [
                    InlineKeyboardButton(
                        text=f"{report['date']} | {report['usernames_count']}",
                        callback_data=f"pick_spam_rep_{report['id']}",
                    )
                ]
            )

        kb.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

        await bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text="Выберите базу для рассылки",
            reply_markup=keyboard,
        )

        await state.set_state(CreateNewTask.msg_text)


@router.message(CreateNewTask.group_identifier)
async def create_task(message: Message, state: FSMContext, user_id: int, bot: Bot):
    group_identifier = message.text.strip()

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    if not group_identifier:
        await message.answer("Идентификатор группы не может быть пустым.")
        return

    data = await state.get_data()
    task_type = data.get("task_type")

    if task_type == "parse":
        try:
            await bot.edit_message_text(
                text="Задача успешно создана!",
                chat_id=message.chat.id,
                message_id=data.get("msg_id", message.message_id),
                reply_markup=await get_back_to_main_kb(),
            )
            response = await create_parse_task(group_identifier, user_id)
        except Exception as e:
            await message.answer(f"Произошла ошибка: {str(e)}")

    await state.clear()


@router.callback_query(CreateNewTask.msg_text)
async def get_msg_text_for_spam(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    dataset_id = call.data.split("pick_spam_rep_")[-1]

    await state.update_data(
        {"dataset_id": dataset_id, "msg_id": call.message.message_id}
    )

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="Напишите текст для рассылки",
        reply_markup=await get_cancel_menu(),
    )

    await state.set_state(CreateNewTask.accept_spam)


@router.message(CreateNewTask.accept_spam)
async def accept_spam_for_users(
    msg: Message, bot: Bot, state: FSMContext, user_id: int
):
    if F.text:
        data = await state.get_data()

        dataset_info = await get_report_info(data["dataset_id"])

        dataset_path = dataset_info["path"]
        worker_id = user_id
        messages_count = 2
        msg_text = msg.text

        await bot.delete_message(chat_id=user_id, message_id=msg.message_id)

        await create_spam_task(dataset_path, worker_id, messages_count, msg_text)

        await bot.edit_message_text(
            chat_id=user_id,
            message_id=data["msg_id"],
            text="Вы успешно запустили рассылку!",
            reply_markup=await get_back_to_main_kb(),
        )

        await state.clear()
