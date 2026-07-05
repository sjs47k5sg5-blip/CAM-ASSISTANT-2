from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_MEMORY, CamState

router = Router()


# =========================
# GET / INIT STATE
# =========================
def get_state(user_id: int) -> CamState:
    if user_id not in CAM_MEMORY:
        CAM_MEMORY[user_id] = CamState()
    return CAM_MEMORY[user_id]


# =========================
# START CAM
# =========================
@router.message(F.text == "⚙ CAM")
async def cam_start(message: Message):
    state = get_state(message.from_user.id)

    await message.answer(
        "CAM активирован\n"
        "Выберите операцию (Контур / Радиус / Фаска)"
    )


# =========================
# TOOL DIAMETER
# =========================
@router.message(F.text.regexp(r"^\d+$"))
async def set_tool(message: Message):

    state = get_state(message.from_user.id)
    state.tool = int(message.text)

    await message.answer(f"✔ Инструмент установлен: {state.tool} мм")


# =========================
# ZERO SELECTION
# =========================
@router.message(F.text.in_(["Центр", "ЛВ угол", "ПВ угол", "ЛН угол", "ПН угол"]))
async def set_zero(message: Message):

    state = get_state(message.from_user.id)

    mapping = {
        "Центр": "CENTER",
        "ЛВ угол": "TL",
        "ПВ угол": "TR",
        "ЛН угол": "BL",
        "ПН угол": "BR"
    }

    state.zero = mapping[message.text]

    await message.answer(f"✔ Ноль детали: {message.text}")


# =========================
# CORNER TYPE
# =========================
@router.message(F.text.in_(["Острые", "Радиус", "Фаска"]))
async def set_corner_type(message: Message):

    state = get_state(message.from_user.id)

    state.corner_type = message.text

    await message.answer(f"✔ Тип углов: {state.corner_type}")


# =========================
# CORNER VALUE (radius/chamfer)
# =========================
@router.message(F.text.regexp(r"^\d+(\.\d+)?$"))
async def set_corner_value(message: Message):

    state = get_state(message.from_user.id)

    value = float(message.text)

    # если это не инструмент (уже был обработан выше)
    if value > 0:
        state.corner_value = value

        await message.answer(f"✔ Параметр (R/Фаска): {value}")


# =========================
# GENERATE G-CODE
# =========================
@router.message(F.text == "Сгенерировать")
async def generate(message: Message):

    state = get_state(message.from_user.id)

    from services.cam_engine import contour

    gcode = contour(
        x=40,
        y=30,
        depth=state.depth,
        stepdown=state.stepdown,
        tool=state.tool,
        zero=state.zero,
        allowance=state.allowance,
        step=0,
        corner_type=state.corner_type,
        corner_value=state.corner_value
    )

    await message.answer(f"<pre>{gcode}</pre>", parse_mode="HTML")


# =========================
# STATUS DEBUG (очень полезно)
# =========================
@router.message(F.text == "📊 Статус")
async def status(message: Message):

    state = get_state(message.from_user.id)

    await message.answer(
        f"📌 CAM STATE:\n"
        f"Tool: {state.tool}\n"
        f"Zero: {state.zero}\n"
        f"Depth: {state.depth}\n"
        f"Stepdown: {state.stepdown}\n"
        f"Corner: {state.corner_type}\n"
        f"Value: {state.corner_value}"
    )