from aiogram.fsm.state import StatesGroup, State


class SetNickname(StatesGroup):
    NICKNAME = State()


class SetBirthday(StatesGroup):
    BIRTHDAY = State()
