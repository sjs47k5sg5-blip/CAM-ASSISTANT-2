from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_DB, CamState
from keyboards.cam_wizard import wizard_zero, wizard_corner_type, wizard_params

router = Router()


def state(uid: int) -> CamState:
    if uid not in CAM_DB:
        CAM_DB[uid] = CamState()
    return CAM_DB[uid]


# =========================
# 1. КОНТУР
# =========================
@router.message(F.text == "📐 Контур")
async def contour(message: Message):

    u = state(message.from_user.id)
    u.mode = "CONTOUR"
    u.step = 1

    await message.answer(
        "✔ Контур выбран\n👉 Шаг 2: выбери ноль детали",
        reply_markup=wizard_zero()
    )


# =========================
# 2. НОЛЬ ДЕТАЛИ
# =========================
@router.message(F.text.in_(["🎯 Центр", "↖ ЛВ", "↗ ПВ", "↙ ЛН", "↘ ПН"]))
async def zero(message: Message):

    u = state(message.from_user.id)
    u.zero = message.text
    u.step = 2

    await message.answer(
        "✔ Ноль установлен\n👉 Шаг 3: тип углов",
        reply_markup=wizard_corner_type()
    )


# =========================
# 3. ТИП УГЛОВ
# =========================
@router.message(F.text.in_(["⬜ Острые", "⭕ Радиус", "📐 Фаска"]))
async def corner_type(message: Message):

    u = state(message.from_user.id)
    u.mode_corner = message.text
    u.step = 3

    await message.answer(
        "✔ Тип углов выбран\n👉 Шаг 4: параметры",
        reply_markup=wizard_params()
    )


# =========================
# 4. ИНСТРУМЕНТ
# =========================
@router.message(F.text.regexp(r"^\d+$"))
async def tool(message: Message):

    u = state(message.from_user.id)
    u.tool = int(message.text)

    await message.answer("✔ Инструмент сохранён\n👉 Введи значение R/Фаски")


# =========================
# 5. ЗНАЧЕНИЕ R / ФАСКИ
# =========================
@router.message(F.text.regexp(r"^\d+(\.\d+)?$"))
async def value(message: Message):

    u = state(message.from_user.id)
    u.corner_value = float(message.text)

    await message.answer("✔ Параметр сохранён\n👉 Можно генерировать")


# =========================
# 6. ГЕНЕРАЦИЯ
# =========================
@router.message(F.text == "✅ Сгенерировать")
async def generate(message: Message):

    u = state(message.from_user.id)

    from services.cam_engine import contour

    gcode = contour(
        x=40,
        y=30,
        depth=5,
        stepdown=2,
        tool=u.tool,
        zero=u.zero,
        allowance=0.2,
        step=0,
        corner_type=u.mode_corner,
        corner_value=u.corner_value
    )

    await message.answer(f"<pre>{gcode}</pre>", parse_mode="HTML")