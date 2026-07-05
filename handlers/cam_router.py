from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
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
# CAM ENTRY (FROM MENU)
# =========================

async def show_milling_menu(message: Message):

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📐 Контур", callback_data="cam_contour")],
        [InlineKeyboardButton(text="🟦 Торец", callback_data="cam_face")],
        [InlineKeyboardButton(text="⬜ Карман", callback_data="cam_pocket")],
        [InlineKeyboardButton(text="➖ Паз", callback_data="cam_slot")],
        [InlineKeyboardButton(text="🌀 Винтовая", callback_data="cam_helical")]
    ])

    await message.answer("Выберите операцию:", reply_markup=kb)


# =========================
# CONTOUR START
# =========================

@router.callback_query(F.data == "cam_contour")
async def contour_start(callback: CallbackQuery, state: FSMContext):

    await callback.answer()
    await state.clear()

    await callback.message.answer("📐 Контур\nВведите ширину (X):")
    await state.set_state(CAMState.width)


# =========================
# WIDTH
# =========================

@router.message(CAMState.width)
async def get_width(message: Message, state: FSMContext):

    try:
        await state.update_data(width=float(message.text))
    except:
        await message.answer("❌ Введите число")
        return

    await message.answer("📏 Введите высоту (Y):")
    await state.set_state(CAMState.height)


# =========================
# HEIGHT
# =========================

@router.message(CAMState.height)
async def get_height(message: Message, state: FSMContext):

    try:
        await state.update_data(height=float(message.text))
    except:
        await message.answer("❌ Введите число")
        return

    await message.answer("📉 Шаг по глубине:")
    await state.set_state(CAMState.step)


# =========================
# STEP
# =========================

@router.message(CAMState.step)
async def get_step(message: Message, state: FSMContext):

    try:
        await state.update_data(step=float(message.text))
    except:
        await message.answer("❌ Введите число")
        return

    await message.answer("📦 Толщина заготовки:")
    await state.set_state(CAMState.thickness)


# =========================
# THICKNESS
# =========================

@router.message(CAMState.thickness)
async def get_thickness(message: Message, state: FSMContext):

    try:
        await state.update_data(thickness=float(message.text))
    except:
        await message.answer("❌ Введите число")
        return

    await message.answer("⬆️ Верх детали / ⬇️ Низ детали")
    await state.set_state(CAMState.zero_mode)


# =========================
# ZERO MODE + GENERATION
# =========================

@router.message(CAMState.zero_mode)
async def generate_gcode(message: Message, state: FSMContext):

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
        caption="CAM CORE CLEAN UI"
    )

    await state.clear()