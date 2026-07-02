from aiogram.fsm.state import StatesGroup, State


class MillingState(StatesGroup):

    manufacturer = State()

    material = State()

    tool = State()

    diameter = State()

    teeth = State()