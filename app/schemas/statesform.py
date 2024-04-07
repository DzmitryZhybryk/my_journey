from aiogram.fsm.state import StatesGroup, State


class LoadTrip(StatesGroup):
    LANGUAGE = State()
    FIRST_PLACE = State()
    LAST_PLACE = State()
    TRANSPORT_TYPE = State()
    TRAVEL_YEAR = State()