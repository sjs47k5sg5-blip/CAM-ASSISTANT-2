from aiogram.fsm.state import State, StatesGroup


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


# ==========================
# Контур
# ==========================

class ContourState(StatesGroup):
    type = State()          # Наружный / Внутренний
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
    side = State()


# ==========================
# Карман
# ==========================

class PocketState(StatesGroup):
    material = State()
    tool = State()
    diameter = State()
    teeth = State()
    length = State()
    width = State()
    depth = State()
    step = State()
    rpm = State()
    overlap = State()
    strategy = State()


# ==========================
# Паз
# ==========================

class SlotState(StatesGroup):
    material = State()
    tool = State()
    diameter = State()
    teeth = State()
    length = State()
    depth = State()
    step = State()
    rpm = State()


# ==========================
# Винтовая интерполяция
# ==========================

class HelixState(StatesGroup):
    material = State()
    tool = State()
    cutter_diameter = State()
    hole_diameter = State()
    depth = State()
    step = State()
    rpm = State()


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