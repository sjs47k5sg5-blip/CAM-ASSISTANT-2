from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_DB, CamState
from keyboards.cam_wizard import wizard_type

router = Router()


# =========================
# STATE
# =========================
def state(uid: int) -> CamState:
    if uid not in CAM_DB:
        CAM_DB[uid] = CamState()
    return CAM_DB[uid]


# =========================
# /START
# =========================
@router.message(F.text == "/start")
async def start(message: Message):

    u = state(message.from_user.id)
    u.step = 0

    await message.answer(
        "🚀 CAM WIZARD запущен\nВыберите тип обработки:",
        reply_markup=wizard_type()
    )


# =========================
# 🔥 BUTTON HANDLERS (ВАЖНО)
# =========================
@router.message(F.text == "📐 Контур")
async def contour(message: Message):
    u = state(message.from_user.id)
    u.mode = "CONTOUR"

    await message.answer("✔ Контур выбран\nВведите диаметр инструмента:")


@router.message(F.text == "🔵 Радиус")
async def radius(message: Message):
    u = state(message.from_user.id)
    u.mode = "RADIUS"

    await message.answer("✔ Радиус выбран\nВведите значение радиуса:")


@router.message(F.text == "📏 Фаска")
async def chamfer(message: Message):
    u = state(message.from_user.id)
    u.mode = "CHAMFER"

    await message.answer("✔ Фаска выбрана\nВведите значение фаски:")


# =========================
# BACK BUTTON
# =========================
@router.message(F.text == "⬅️ Назад")
async def back(message: Message):
    await message.answer(
        "↩ Возврат в CAM:",
        reply_markup=wizard_type()
    )


# =========================
# TOOL INPUT
# =========================
@router.message(F.text.regexp(r"^\d+$"))
async def tool_input(message: Message):

    u = state(message.from_user.id)

    u.tool = int(message.text)
    u.step = 1

    await message.answer(f"✔ Инструмент: {u.tool} мм\nПродолжай настройки")


# =========================
# VALUE INPUT (R / CHAMFER)
# =========================
@router.message(F.text.regexp(r"^\d+(\.\d+)?$"))
async def value_input(message: Message):

    u = state(message.from_user.id)

    u.corner_value = float(message.text)

    await message.answer(
        f"✔ Значение сохранено: {u.corner_value}\nТеперь можно генерировать"
    )


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
        corner_type=u.mode,
        corner_value=u.corner_value
    )

    await message.answer(f"<pre>{gcode}</pre>", parse_mode="HTML")