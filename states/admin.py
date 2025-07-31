from aiogram.fsm.state import StatesGroup, State


class GetNewToken(StatesGroup):
    token_name = State()
