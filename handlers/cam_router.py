from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from services.contour_gcode import contour_gcode
from services.cam_engine import CAMEngine
from services.ui_state import ui_state

router = Router()
engine = CAMEngine()


# =========================
# FSM
# =========================

class CAMState(StatesGroup):
    width = State()
    height = State()
    step = State()
    thickness = State()


# =========================
# CAM MENU (SAFE UI)
# =========================

async def show_milling_menu(message: Message):

    if ui_state.is_menu_open("milling"):
        return

    ui_state.set_menu("milling")

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📐 Контур", callback_data="cam_contour")],
        [InlineKeyboardButton(text="🟦 Торец", callback_data="cam_face")],
        [InlineKeyboardButton(text="⬜ Карман", callback_data="cam_pocket")],
        [InlineKeyboardButton(text="➖ Паз", callback_data="cam_slot")],
        [InlineKeyboardButton(text="🌀 Винтовая", callback_data="cam_helical")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="cam_back")]
    ])

    await message.answer("📌 Выберите операцию:", reply_markup=kb)


# =========================
# BACK
# =========================

@router.callback_query(F.data == "cam_back")
async def back(callback: CallbackQuery):

    await callback.answer()
    ui_state.reset()
    await callback.message.answer("↩️ Главное меню")


# =========================
# CONTOUR START
# =========================

@router.callback_query(F.data == "cam_contour")
async def contour_start(callback: CallbackQuery, state: FSMContext):

    await callback.answer()
    ui_state.set_menu("contour")

    await state.clear()

    await callback.message.answer("📐 Контур\nВведите ширину (X):")
    await state.set_state(CAMState.width)


# =========================
# WIDTH
# =========================

@router.message(CAMState.width)
async def width(message: Message, state: FSMContext):

    if not message.text.replace('.', '', 1).isdigit():
        await message.answer("❌ Введите число")
        return

    await state.update_data(width=float(message.text))
    await message.answer("📏 Введите высоту (Y):")
    await state.set_state(CAMState.height)


# =========================
# HEIGHT
# =========================

@router.message(CAMState.height)
async def height(message: Message, state: FSMContext):

    if not message.text.replace('.', '', 1).isdigit():
        await message.answer("❌ Введите число")
        return

    await state.update_data(height=float(message.text))
    await message.answer("📉 Шаг по глубине:")
    await state.set_state(CAMState.step)


# =========================
# STEP
# =========================

@router.message(CAMState.step)
async def step(message: Message, state: FSMContext):

    if not message.text.replace('.', '', 1).isdigit():
        await message.answer("❌ Введите число")
        return

    await state.update_data(step=float(message.text))
    await message.answer("📦 Толщина заготовки:")
    await state.set_state(CAMState.thickness)


# =========================
# THICKNESS + ZERO MODE (BUTTONS)
# =========================

def zero_mode_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬆️ Верх детали", callback_data="zero_top")],
        [InlineKeyboardButton(text="⬇️ Низ детали", callback_data="zero_bottom")]
    ])


@router.message(CAMState.thickness)
async def thickness(message: Message, state: FSMContext):

    if not message.text.replace('.', '', 1).isdigit():
        await message.answer("❌ Введите число")
        return

    data = await state.get_data()
    data["thickness"] = float(message.text)

    cam_plan = engine.build(data)
    await state.update_data(cam_plan=cam_plan)

    await message.answer(
        "📍 Выберите ноль детали:",
        reply_markup=zero_mode_keyboard()
    )


# =========================
# ZERO MODE HANDLER (FINAL STEP)
# =========================

@router.callback_query(F.data.in_(["zero_top", "zero_bottom"]))
async def zero_mode(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    data = await state.get_data()

    zero_mode = "top" if callback.data == "zero_top" else "bottom"

    cam_plan = data.get("cam_plan", {})

    gcode = contour_gcode(
        width=data["width"],
        height=data["height"],
        depth_step=data["step"],
        final_depth=data["thickness"],
        thickness=data["thickness"],
        zero_mode=zero_mode,
        cam_plan=cam_plan
    )

    await callback.message.answer("✅ G-code готов")

    await callback.message.answer_document(
        document=gcode.encode("utf-8"),
        caption="CAM CORE PRO FIX"
    )

    await state.clear()
    ui_state.reset()