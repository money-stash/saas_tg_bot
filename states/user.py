from aiogram.fsm.state import StatesGroup, State


class Login(StatesGroup):
    login_key = State()
