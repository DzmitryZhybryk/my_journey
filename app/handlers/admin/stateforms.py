from aiogram.fsm.state import StatesGroup, State


class ChangeRole(StatesGroup):
    UserID = State()
    ROLE = State()

