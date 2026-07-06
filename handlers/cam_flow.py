from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_DB, CamState

router = Router()


def state(uid: int) -> CamState:
    if uid not in CAM_DB:
        CAM_DB[uid] = CamState()
    return CAM_DB[uid]


# =========================
# ENTRY FROM BUTTON
# =========================
@router.message(F.text == "📐 Контур")
async def contour(message: Message):
    u = state(message.from_user.id)
    u.step = 1
    await message.answer("📏 Введите X Y Z (например: 30 30 30)")


# =========================
# SIZE
# =========================
@router.message(F.text.regexp(r"^\d+ \d+ \d+$"))
async def size(message: Message):
    u = state(message.from_user.id)

    if u.step != 1:
        return

    x, y, z = message.text.split()

    u.x = float(x)
    u.y = float(y)
    u.z = float(z)

    u.step = 2
    await message.answer("🔧 Введите диаметр инструмента")


# =========================
# TOOL
# =========================
@router.message(F.text.regexp(r"^\d+(\.\d+)?$"))
async def tool(message: Message):
    u = state(message.from_user.id)

    if u.step != 2:
        return

    u.tool_d = float(message.text)
    u.step = 3

    await message.answer("📍 Ноль детали: CENTER / TL / TR / BL / BR")


# =========================
# ZERO
# =========================
@router.message(F.text.in_(["CENTER","TL","TR","BL","BR"]))
async def zero(message: Message):
    u = state(message.from_user.id)

    if u.step != 3:
        return

    u.zero = message.text
    u.step = 4

    await message.answer("📍 Ноль Z: TOP / BOTTOM")


# =========================
# ZERO Z
# =========================
@router.message(F.text.in_(["TOP","BOTTOM"]))
async def zeroz(message: Message):
    u = state(message.from_user.id)

    if u.step != 4:
        return

    u.zero_z = message.text
    u.step = 5

    await message.answer("⚙ Углы: Все / ЛВ / ЛН / ПВ / ПН")


# =========================
# CORNER TARGET
# =========================
@router.message(F.text.in_(["Все","ЛВ","ЛН","ПВ","ПН"]))
async def corner_target(message: Message):
    u = state(message.from_user.id)

    if u.step != 5:
        return

    u.corner_target = message.text
    u.step = 6

    await message.answer("Введите: радиус / фаска / острые")


# =========================
# CORNER TYPE
# =========================
@router.message(F.text.in_(["радиус","фаска","острые"]))
async def corner_type(message: Message):
    u = state(message.from_user.id)

    if u.step != 6:
        return

    u.corner_mode = message.text.upper()
    u.step = 7

    await message.answer("Введите значение (мм)")


# =========================
# VALUE
# =========================
@router.message(F.text.regexp(r"^\d+(\.\d+)?$"))
async def value(message: Message):
    u = state(message.from_user.id)

    if u.step != 7:
        return

    u.corner_value = float(message.text)
    u.step = 8

    await message.answer("✔ Готово → ГЕНЕРАЦИЯ")


# =========================
# GENERATE
# =========================
@router.message(F.text == "ГЕНЕРАЦИЯ")
async def generate(message: Message):

    u = state(message.from_user.id)

    from services.cam_engine import contour

    gcode = contour(
        x=u.x,
        y=u.y,
        depth=u.z,
        stepdown=2,
        tool=u.tool_d,
        zero=u.zero,
        allowance=0.2,
        step=0,
        corner_type=u.corner_mode,
        corner_value=u.corner_value
    )

    await message.answer(f"<pre>{gcode}</pre>", parse_mode="HTML")