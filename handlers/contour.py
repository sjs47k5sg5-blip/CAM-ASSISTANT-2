from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from services.contour_gcode import contour_gcode

router = Router()


# =========================
# STATES
# =========================

class ContourState(StatesGroup):
    width = State()
    height = State()
    depth = State()
    thickness = State()
    zero_mode = State()


# =========================
# START CONTROLLER
# =========================

@router.message(F.text == "📐 Контур")
async def start_contour(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Введи ширину (X):")
    await state.set_state(ContourState.width)


# =========================
# WIDTH
# =========================

@router.message(ContourState.width)
async def get_width(message: Message, state: FSMContext):
    await state.update_data(width=float(message.text))
    await message.answer("Введи высоту (Y):")
    await state.set_state(ContourState.height)


# =========================
# HEIGHT
# =========================

@router.message(ContourState.height)
async def get_height(message: Message, state: FSMContext):
    await state.update_data(height=float(message.text))
    await message.answer("Введи шаг по глубине (например 3):")
    await state.set_state(ContourState.depth)


# =========================
# DEPTH STEP
# =========================

@router.message(ContourState.depth)
async def get_depth(message: Message, state: FSMContext):
    await state.update_data(depth_step=float(message.text))
    await message.answer("Введи толщину заготовки (Z size):")
    await state.set_state(ContourState.thickness)


# =========================
# THICKNESS
# =========================

@router.message(ContourState.thickness)
async def get_thickness(message: Message, state: FSMContext):
    await state.update_data(thickness=float(message.text))

    # выбор zero mode
    kb_text = (
        "Выбор нуля детали:\n\n"
        "⬆️ Верх детали\n"
        "⬇️ Низ детали"
    )

    await message.answer(kb_text)
    await state.set_state(ContourState.zero_mode)


# =========================
# ZERO MODE + GENERATION
# =========================

@router.message(ContourState.zero_mode)
async def get_zero_mode(message: Message, state: FSMContext):
    data = await state.get_data()

    zero_mode = message.text

    width = data["width"]
    height = data["height"]
    depth_step = data["depth_step"]
    thickness = data["thickness"]

    # =========================
    # GENERATE GCODE
    # =========================

    gcode = contour_gcode(
        width=width,
        height=height,
        depth_step=depth_step,
        final_depth=thickness,
        zero_mode=zero_mode,
        thickness=thickness
    )

    await message.answer("✅ G-code готов")
    
    # если длинный -- отправляем файлом
    await message.answer_document(
        document=gcode.encode("utf-8"),
        caption="CAM FIX v3 ZERO Z"
    )

    await state.clear()