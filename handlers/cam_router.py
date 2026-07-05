from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from services.contour_gcode import contour_gcode

router = Router()


# =========================
# FSM STATES
# =========================

class CAMState(StatesGroup):
    width = State()
    height = State()
    step = State()
    thickness = State()
    zero_mode = State()


# =========================
# ENTRY POINT (ALL CAM OPS)
# =========================

@router.callback_query(F.data == "cam_contour")
async def start_contour(callback: CallbackQuery, state: FSMContext):

    await callback.answer()
    await state.clear()

    await callback.message.answer("📐 Контур\nВведи ширину (X):")
    await state.set_state(CAMState.width)


# =========================
# WIDTH
# =========================

@router.message(CAMState.width)
async def get_width(message: Message, state: FSMContext):

    try:
        await state.update_data(width=float(message.text))
    except:
        await message.answer("❌ Введи число")
        return

    await message.answer("📐 Введи высоту (Y):")
    await state.set_state(CAMState.height)


# =========================
# HEIGHT
# =========================

@router.message(CAMState.height)
async def get_height(message: Message, state: FSMContext):

    try:
        await state.update_data(height=float(message.text))
    except:
        await message.answer("❌ Введи число")
        return

    await message.answer("📉 Введи шаг по глубине:")
    await state.set_state(CAMState.step)


# =========================
# STEP
# =========================

@router.message(CAMState.step)
async def get_step(message: Message, state: FSMContext):

    try:
        await state.update_data(step=float(message.text))
    except:
        await message.answer("❌ Введи число")
        return

    await message.answer("📏 Введи толщину заготовки:")
    await state.set_state(CAMState.thickness)


# =========================
# THICKNESS
# =========================

@router.message(CAMState.thickness)
async def get_thickness(message: Message, state: FSMContext):

    try:
        await state.update_data(thickness=float(message.text))
    except:
        await message.answer("❌ Введи число")
        return

    await message.answer(
        "⬆️ Верх детали\n⬇️ Низ детали"
    )
    await state.set_state(CAMState.zero_mode)


# =========================
# ZERO MODE + GENERATE GCODE
# =========================

@router.message(CAMState.zero_mode)
async def generate(message: Message, state: FSMContext):

    data = await state.get_data()

    zero_mode = message.text

    # =========================
    # NORMALIZE ZERO MODE
    # =========================

    if zero_mode in ["⬆️ Верх детали", "top"]:
        zero_mode = "top"
    else:
        zero_mode = "bottom"

    # =========================
    # GENERATE GCODE
    # =========================

    gcode = contour_gcode(
        width=data["width"],
        height=data["height"],
        depth_step=data["step"],
        final_depth=data["thickness"],
        thickness=data["thickness"],
        zero_mode=zero_mode
    )

    await message.answer("✅ G-code готов")

    await message.answer_document(
        document=gcode.encode("utf-8"),
        caption="CAM CORE ROUTER v1"
    )

    await state.clear()