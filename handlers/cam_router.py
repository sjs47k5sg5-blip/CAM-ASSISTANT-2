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
# FSM ONLY INPUTS
# =========================

class CAMState(StatesGroup):
    width = State()
    height = State()
    step = State()
    thickness = State()


# =========================
# START CONTROLLER
# =========================

@router.callback_query(F.data == "cam_contour")
async def start(callback: CallbackQuery, state: FSMContext):

    await callback.answer()
    await state.clear()

    ui_state.set_menu("contour")

    await callback.message.answer("📐 Введите ширину (X):")
    await state.set_state(CAMState.width)


# =========================
# WIDTH
# =========================

@router.message(CAMState.width)
async def width(message: Message, state: FSMContext):

    await state.update_data(width=float(message.text))
    await message.answer("📏 Введите высоту (Y):")
    await state.set_state(CAMState.height)


# =========================
# HEIGHT
# =========================

@router.message(CAMState.height)
async def height(message: Message, state: FSMContext):

    await state.update_data(height=float(message.text))
    await message.answer("📉 Шаг по глубине:")
    await state.set_state(CAMState.step)


# =========================
# STEP
# =========================

@router.message(CAMState.step)
async def step(message: Message, state: FSMContext):

    await state.update_data(step=float(message.text))
    await message.answer("📦 Толщина заготовки:")
    await state.set_state(CAMState.thickness)


# =========================
# THICKNESS → ZERO MENU
# =========================

def zero_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬆️ Верх детали", callback_data="zero_top")],
        [InlineKeyboardButton(text="⬇️ Низ детали", callback_data="zero_bottom")]
    ])


@router.message(CAMState.thickness)
async def thickness(message: Message, state: FSMContext):

    data = await state.get_data()
    data["thickness"] = float(message.text)

    cam_plan = engine.build(data)

    await state.update_data(cam_plan=cam_plan)

    await message.answer("📍 Выберите ноль детали:", reply_markup=zero_keyboard())


# =========================
# ZERO MODE (CLEAN CALLBACK)
# =========================

@router.callback_query(F.data.in_(["zero_top", "zero_bottom"]))
async def zero(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    data = await state.get_data()

    zero_mode = "top" if callback.data == "zero_top" else "bottom"

    gcode = contour_gcode(
        width=data["width"],
        height=data["height"],
        depth_step=data["step"],
        final_depth=data["thickness"],
        thickness=data["thickness"],
        zero_mode=zero_mode,
        cam_plan=data.get("cam_plan", {})
    )

    await callback.message.answer("✅ G-code готов")

    await callback.message.answer_document(
        document=gcode.encode("utf-8"),
        caption="CAM FSM v2 CLEAN"
    )

    await state.clear()
    ui_state.reset()