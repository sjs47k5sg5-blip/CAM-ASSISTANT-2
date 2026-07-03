from aiogram.fsm.state import State, StatesGroup


# ==========================
# Проект
# ==========================

class ProjectState(StatesGroup):
    name = State()
    material = State()


# ==========================
# Режимы резания
# ==========================

class MillingState(StatesGroup):
    material = State()
    tool = State()
    diameter = State()
    teeth = State()


# ==========================
# Торцевое фрезерование
# ==========================

class FaceState(StatesGroup):
    material = State()
    tool = State()
    diameter = State()
    teeth = State()
    width = State()
    length = State()
    depth = State()
    rpm = State()
    overlap = State()
    strategy = State()
    zero = State()


# ==========================
# Контур
# ==========================

class ContourState(StatesGroup):
    type = State()
    material = State()
    tool = State()
    diameter = State()
    teeth = State()
    length = State()
    width = State()
    depth = State()
    step = State()
    rpm = State()
    allowance = State()
    direction = State()
    zero = State()


# ==========================
# Сверление
# ==========================

class DrillingState(StatesGroup):
    material = State()
    tool = State()
    diameter = State()
    depth = State()


# ==========================
# Нарезание резьбы
# ==========================

class ThreadState(StatesGroup):
    thread = State()
    depth = State()
    rpm = State()


# ==========================
# Допуски
# ==========================

class ToleranceState(StatesGroup):
    field = State()
    diameter = State()