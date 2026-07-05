from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_DB, CamState

router = Router()


# =========================
# GET STATE
# =========================
def state(uid: int) -> CamState:
    if uid not in CAM_DB:
        CAM_DB[uid] = CamState()
    return CAM_DB[uid]


# =========================
# STEP LOCK (важно!)
# =========================
def require_step(user: CamState, step: int):
    return user.step == step


# =========================
# STEP 1: TOOL
# =========================
@router.message(F.text.regexp(r"^\d+$"))
async def tool_input(message: Message):

    u = state(message.from_user.id)

    if u.step != 0:
        return

    u.tool = int(message.text)
    u.step = 1

    await message.answer("✔ Инструмент сохранён\n👉 Шаг 2: выбери ноль детали")


# =========================
# STEP 2: ZERO
# =========================
@router.message(F.text.in_(["Центр", "ЛВ", "ПВ", "ЛН", "ПН"]))
async def zero_input(message: Message):

    u = state(message.from_user.id)

    if u.step != 1:
        return

    mapping = {
        "Центр": "CENTER",
        "ЛВ": "TL",
        "ПВ": "TR",
        "ЛН": "BL",
        "ПН": "BR"
    }

    u.zero = mapping[message.text]
    u.step = 2

    await message.answer("✔ Ноль установлен\n👉 Шаг 3: тип углов")


# =========================
# STEP 3: CORNER TYPE
# =========================
@router.message(F.text.in_(["Острые", "Радиус", "Фаска"]))
async def corner_type(message: Message):

    u = state(message.from_user.id)

    if u.step != 2:
        return

    u.corner_type = message.text.upper()
    u.step = 3

    await message.answer("✔ Тип углов выбран\n👉 Шаг 4: значение")


# =========================
# STEP 4: VALUE
# =========================
@router.message(F.text.regexp(r"^\d+(\.\d+)?$"))
async def value(message: Message):

    u = state(message.from_user.id)

    if u.step != 3:
        return

    u.corner_value = float(message.text)
    u.step = 4

    await message.answer("✔ Параметр сохранён\n👉 Готов к генерации")


# =========================
# GENERATE (FINAL LOCK)
# =========================
@router.message(F.text == "Сгенерировать")
async def generate(message: Message):

    u = state(message.from_user.id)

    if u.tool == 0 or u.zero == "":
        await message.answer("❌ CAM не заполнен")
        return

    from services.cam_engine import contour

    gcode = contour(
        x=40,
        y=30,
        depth=u.depth or 5,
        stepdown=u.stepdown or 2,
        tool=u.tool,
        zero=u.zero,
        allowance=u.allowance or 0.2,
        step=0,
        corner_type=u.corner_type,
        corner_value=u.corner_value
    )

    u.step = 0

    await message.answer(f"<pre>{gcode}</pre>", parse_mode="HTML")