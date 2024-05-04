from aiogram.fsm.state import StatesGroup, State


class LoadTrip(StatesGroup):
    FIRST_PLACE = State()
    LAST_PLACE = State()
    TRANSPORT_TYPE = State()
    TRAVEL_YEAR = State()


class DeleteTrip(StatesGroup):
    TRAVEL_ID = State()
