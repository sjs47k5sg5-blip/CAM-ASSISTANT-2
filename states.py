from aiogram.fsm.state import StatesGroup, State


class MillingState(StatesGroup):
    diameter = State()
    teeth = State()
    vc = State()
    fz = State()