from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_DB, CamState

router = Router()


def state(uid: int) -> CamState:
    if uid not in CAM_DB:
        CAM_DB[uid] = CamState()
    return CAM_DB[uid]


# =========================
# ENTRY CAM
# =========================
@router.message(F.text == "⚙ Фрезерные операции")
async def cam_start(message: Message):
    await message.answer("👉 Нажмите 📐 Контур")


# =========================
# CONTOUR (🔥 FIXED)
# =========================
@router.message(F.text == "📐 Контур")
async def contour(message: Message):
    u = state(message.from_user.id)
    u.step = 1
    await message.answer("📏 Введите размер детали: X Y Z")


# =========================
# SIZE
# =========================
@router.message(F.text.regexp(r"^\d+ \d+ \d+$"))
async def size(message: Message):
    u = state(message.from_user.id)

    if u.step != 1:
        return

    x, y, z = message.text.split()

    u.size_x = float(x)
    u.size_y = float(y)
    u.size_z = float(z)

    u.step = 2

    await message.answer("🔧 Введите инструмент")


# =========================
# TOOL
# =========================
@router.message(F.text.regexp(r"^\d+(\.\d+)?$"))
async def tool(message: Message):
    u = state(message.from_user.id)

    if u.step != 2:
        return

    u.tool = float(message.text)
    u.step = 3

    await message.answer("📐 Введите R / фаску")


# =========================
# VALUE
# =========================
@router.message(F.text.regexp(r"^\d+(\.\d+)?$"))
async def value(message: Message):
    u = state(message.from_user.id)

    if u.step != 3:
        return

    u.corner_value = float(message.text)
    u.step = 4

    await message.answer("✅ Готово → ГЕНЕРАЦИЯ")


# =========================
# GENERATE
# =========================
@router.message(F.text == "ГЕНЕРАЦИЯ")
async def generate(message: Message):
    u = state(message.from_user.id)

    from services.cam_engine import contour

    gcode = contour(
        x=u.size_x,
        y=u.size_y,
        depth=u.size_z,
        tool=u.tool,
        zero=u.zero,
        allowance=0.2,
        stepdown=2,
        corner_type=u.mode,
        corner_value=u.corner_value
    )

    await message.answer(f"<pre>{gcode}</pre>", parse_mode="HTML")