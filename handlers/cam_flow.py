from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_DB, CamState

router = Router()


def state(uid: int) -> CamState:
    if uid not in CAM_DB:
        CAM_DB[uid] = CamState()
    return CAM_DB[uid]


# =========================
# ENTRY
# =========================
@router.message(F.text == "📐 Контур")
async def contour(message: Message):

    u = state(message.from_user.id)
    u.step = 1

    from keyboards.cam_menu import params_menu

    await message.answer(
        "📐 КОНТУР CAM\n\nВведите параметры обработки",
        reply_markup=params_menu()
    )


# =========================
# SIZE (STEP 2)
# =========================
@router.message(F.text == "📏 Размер детали")
async def size(message: Message):
    u = state(message.from_user.id)
    u.step = 2
    await message.answer("X Y Z")


@router.message(F.text.regexp(r"^\d+ \d+ \d+$"))
async def size_input(message: Message):
    u = state(message.from_user.id)

    if u.step != 2:
        return

    x, y, z = message.text.split()
    u.x, u.y, u.z = float(x), float(y), float(z)

    u.step = 3
    await message.answer("✔ размер OK")


# =========================
# TOOL (STEP 3)
# =========================
@router.message(F.text == "🔧 Инструмент")
async def tool(message: Message):
    u = state(message.from_user.id)
    u.step = 3
    await message.answer("диаметр")


@router.message(F.text.regexp(r"^\d+(\.\d+)?$"))
async def tool_input(message: Message):
    u = state(message.from_user.id)

    if u.step != 3:
        return

    u.tool_d = float(message.text)

    u.step = 4
    await message.answer("✔ инструмент OK")


# =========================
# ZERO
# =========================
@router.message(F.text == "📍 Ноль детали")
async def zero(message: Message):
    u = state(message.from_user.id)
    u.step = 4
    await message.answer("CENTER / TL / TR / BL / BR")


@router.message(F.text.in_(["CENTER","TL","TR","BL","BR"]))
async def zero_set(message: Message):
    u = state(message.from_user.id)

    if u.step != 4:
        return

    u.zero = message.text
    u.step = 5

    await message.answer("✔ zero OK")


# =========================
# ZERO Z
# =========================
@router.message(F.text == "📍 Ноль Z")
async def zeroz(message: Message):
    u = state(message.from_user.id)
    u.step = 5
    await message.answer("TOP / BOTTOM")


@router.message(F.text.in_(["TOP","BOTTOM"]))
async def zeroz_set(message: Message):
    u = state(message.from_user.id)

    if u.step != 5:
        return

    u.zero_z = message.text
    u.step = 6

    await message.answer("✔ Z OK")


# =========================
# CORNERS
# =========================
@router.message(F.text == "⚙ Углы")
async def corners(message: Message):
    u = state(message.from_user.id)
    u.step = 6
    await message.answer("Все / ЛВ / ЛН / ПВ / ПН")


@router.message(F.text.in_(["Все","ЛВ","ЛН","ПВ","ПН"]))
async def corners_target(message: Message):
    u = state(message.from_user.id)

    if u.step != 6:
        return

    u.corner_target = message.text
    u.step = 7

    await message.answer("радиус / фаска / острые")


@router.message(F.text.in_(["радиус","фаска","острые"]))
async def corners_type(message: Message):
    u = state(message.from_user.id)

    if u.step != 7:
        return

    u.corner_mode = message.text.upper()

    await message.answer("значение мм")


@router.message(F.text.regexp(r"^\d+(\.\d+)?$"))
async def corners_value(message: Message):
    u = state(message.from_user.id)

    if u.step != 7:
        return

    u.corner_value = float(message.text)
    u.step = 8

    await message.answer("✔ углы OK")


# =========================
# ALLOWANCE
# =========================
@router.message(F.text == "📉 Припуск")
async def allowance(message: Message):
    await message.answer("0 / 0.2 / 0.5")


@router.message(F.text.in_(["0","0.2","0.5"]))
async def allowance_set(message: Message):
    u = state(message.from_user.id)
    u.allowance = float(message.text)

    await message.answer("✔ припуск OK")


# =========================
# READY
# =========================
@router.message(F.text == "✅ Готово")
async def ready(message: Message):
    await message.answer("Готово → ГЕНЕРАЦИЯ")


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
        allowance=u.allowance,
        step=0,
        corner_type=u.corner_mode,
        corner_value=u.corner_value
    )

    await message.answer(f"<pre>{gcode}</pre>", parse_mode="HTML")