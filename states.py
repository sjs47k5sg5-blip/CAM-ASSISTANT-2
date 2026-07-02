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
    strategy = State()


# ==========================
# Контур
# ==========================

class ContourState(StatesGroup):
    material = State()
    tool = State()
    diameter = State()
    depth = State()
    step = State()
    rpm = State()
    side = State()


# ==========================
# Карман
# ==========================

class PocketState(StatesGroup):
    material = State()
    tool = State()
    diameter = State()
    length = State()
    width = State()
    depth = State()
    step = State()
    rpm = State()
    strategy = State()


# ==========================
# Паз
# ==========================

class SlotState(StatesGroup):
    material = State()
    tool = State()
    diameter = State()
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