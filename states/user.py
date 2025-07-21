from aiogram.fsm.state import StatesGroup, State


class Login(StatesGroup):
    login_key = State()


class UpdateLogin(StatesGroup):
    login_key = State()


class UploadSession(StatesGroup):
    session_file = State()
    json_file = State()


class UpdateAvatar(StatesGroup):
    avatar = State()


class ChangeName(StatesGroup):
    name = State()


class ChangeSurname(StatesGroup):
    surname = State()


class ChangeUsername(StatesGroup):
    username = State()


class CreateNewTask(StatesGroup):
    group_identifier = State()
    task_type = State()
