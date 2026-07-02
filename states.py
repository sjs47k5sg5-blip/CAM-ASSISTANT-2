from aiogram.fsm.state import State, StatesGroup


class MillingState(StatesGroup):
    material = State()
    tool = State()
    diameter = State()
    teeth = State()
    machining = State()
    overhang = State()


class DrillingState(StatesGroup):
    material = State()
    tool = State()
    diameter = State()
    depth = State()