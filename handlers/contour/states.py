from aiogram.fsm.state import State, StatesGroup


class ContourWizard(StatesGroup):

    menu = State()

    size = State()

    material = State()

    zero = State()

    zero_z = State()

    corner_type = State()

    corner_select = State()

    corner_value = State()

    allowance = State()

    finish_pass = State()

    finish_tool = State()

    tool = State()

    step_z = State()

    ready = State()