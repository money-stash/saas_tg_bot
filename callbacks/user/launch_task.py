import json
from aiogram.types import (
    CallbackQuery,
    Message,
)
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from database.db import db
from states.user import CreateNewTask
from api.user_api import (
    create_parse_task,
    get_session_info,
    get_users,
    update_first_name,
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

    else:
        await bot.edit_message_text(
            text="Вы выбрали некорректный тип задачи.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=await get_newtask_types_menu(),
        )


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
    else:
        await message.answer(
            "Выбран некорректный тип задачи.", reply_markup=await get_back_to_main_kb()
        )

    await state.clear()
