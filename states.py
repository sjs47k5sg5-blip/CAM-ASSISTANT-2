from aiogram.fsm.state import State, StatesGroup


# ==========================
# Проект
# ==========================

class ProjectState(StatesGroup):
    name = State()
    material = State()


# ==========================
# Торцевое фрезерование
# ==========================

class FaceState(StatesGroup):
    material = State()
    cutter = State()
    diameter = State()
    width = State()
    length = State()
    depth = State()


# ==========================
# Контур (в разработке)
# ==========================

class ContourState(StatesGroup):
    material = State()
    cutter = State()
    diameter = State()
    width = State()
    length = State()
    depth = State()
    direction = State()


# ==========================
# Сверление
# ==========================

class DrillingState(StatesGroup):
    hole_type = State()
    material = State()
    tool = State()
    tool_number = State()
    diameter = State()
    depth = State()
    work_offset = State()
    r_plane = State()
    coordinates = State()


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
    tolerance = State()
    diameter = State()