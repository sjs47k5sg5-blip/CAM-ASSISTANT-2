from aiogram.fsm.state import State, StatesGroup


class ContourWizard(StatesGroup):

    # ==============================
    # Главное меню
    # ==============================

    menu = State()

    # ==============================
    # Размер детали
    # ==============================

    size = State()

    # ==============================
    # Материал
    # ==============================

    material = State()

    # ==============================
    # Ноль детали
    # ==============================

    zero = State()

    zero_z = State()

    # ==============================
    # Инструмент
    # ==============================

    tool = State()

    # ==============================
    # Мастер обработки
    # ==============================

    processing = State()

    roughing = State()

    step_z = State()

    stepover = State()

    direction = State()

    allowance = State()

    finish = State()

    finish_tool = State()

    corner_type = State()

    corner_position = State()

    corner_value = State()

    # ==============================
    # Генерация
    # ==============================

    ready = State()