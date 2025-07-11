from aiogram.fsm.state import StatesGroup, State


class Login(StatesGroup):
    login_key = State()


class UpdateLogin(StatesGroup):
    login_key = State()


class UploadSession(StatesGroup):
    session_file = State()
    json_file = State()
