from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_DB, CamState
from keyboards.cam_wizard import wizard_type

router = Router()


# =========================
# STATE GET
# =========================
def state(uid: int) -> CamState:
    if uid not in CAM_DB:
        CAM_DB[uid] = CamState()
    return CAM_DB[uid]


# =========================
# /START (ВАЖНО!)
# =========================
@router.message(F.text == "/start")
async def start(message: Message):

    u = state(message.from_user.id)
    u.step = 0

    await message.answer(
        "🚀 CAM WIZARD запущен\n"
        "Шаг 1: выбери тип обработки",
        reply_markup=wizard_type()
    )


# =========================
# TOOL INPUT
# =========================
@router.message(F.text.regexp(r"^\d+$"))
async def tool(message: Message):

    u = state(message.from_user.id)

    if u.step != 0:
        return

    u.tool = int(message.text)
    u.step = 1

    await message.answer("✔ Инструмент сохранён → Шаг 2")


# =========================
# ZERO INPUT
# =========================
@router.message(F.text.in_(["Центр", "ЛВ", "ПВ", "ЛН", "ПН"]))
async def zero(message: Message):

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

    await message.answer("✔ Ноль установлен → Шаг 3")


# =========================
# CORNER TYPE
# =========================
@router.message(F.text.in_(["Острые", "Радиус", "Фаска"]))
async def corner(message: Message):

    u = state(message.from_user.id)

    if u.step != 2:
        return

    u.corner_type = message.text.upper()
    u.step = 3

    await message.answer("✔ Углы выбраны → Шаг 4")


# =========================
# VALUE INPUT
# =========================
@router.message(F.text.regexp(r"^\d+(\.\d+)?$"))
async def value(message: Message):

    u = state(message.from_user.id)

    if u.step != 3:
        return

    u.corner_value = float(message.text)
    u.step = 4

    await message.answer("✔ Параметр сохранён → ГОТОВО")


# =========================
# GENERATE
# =========================
@router.message(F.text == "Сгенерировать")
async def generate(message: Message):

    u = state(message.from_user.id)

    from services.cam_engine import contour

    gcode = contour(
        x=40,
        y=30,
        depth=u.depth,
        stepdown=u.stepdown,
        tool=u.tool,
        zero=u.zero,
        allowance=u.allowance,
        step=0,
        corner_type=u.corner_type,
        corner_value=u.corner_value
    )

    await message.answer(f"<pre>{gcode}</pre>", parse_mode="HTML")