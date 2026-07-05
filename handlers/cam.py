from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from services.gcode import contour

router = Router()


# =========================
# FSM STATES
# =========================
class CAM(StatesGroup):
    x = State()
    y = State()
    step = State()
    depth = State()
    zero = State()


# =========================
# START CAM
# =========================
@router.message(F.text == "Контур")
async def start_cam(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("📐 Введите X:")
    await state.set_state(CAM.x)


# =========================
# X
# =========================
@router.message(CAM.x)
async def x_handler(message: Message, state: FSMContext):
    try:
        x = float(message.text)
    except:
        return await message.answer("❌ Введите число X")

    await state.update_data(x=x)
    await message.answer("📏 Введите Y:")
    await state.set_state(CAM.y)


# =========================
# Y
# =========================
@router.message(CAM.y)
async def y_handler(message: Message, state: FSMContext):
    try:
        y = float(message.text)
    except:
        return await message.answer("❌ Введите число Y")

    await state.update_data(y=y)
    await message.answer("📉 Шаг по глубине:")
    await state.set_state(CAM.step)


# =========================
# STEP
# =========================
@router.message(CAM.step)
async def step_handler(message: Message, state: FSMContext):
    try:
        step = float(message.text)
    except:
        return await message.answer("❌ Введите шаг")

    await state.update_data(step=step)
    await message.answer("📦 Глубина обработки:")
    await state.set_state(CAM.depth)


# =========================
# DEPTH -> ZERO MODE
# =========================
@router.message(CAM.depth)
async def depth_handler(message: Message, state: FSMContext):
    try:
        depth = float(message.text)
    except:
        return await message.answer("❌ Введите глубину")

    await state.update_data(depth=depth)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬆️ Верх детали", callback_data="zero_top")],
        [InlineKeyboardButton(text="⬇️ Низ детали", callback_data="zero_bottom")]
    ])

    await message.answer("📍 Выбор нуля:", reply_markup=kb)
    await state.set_state(CAM.zero)


# =========================
# ZERO MODE
# =========================
@router.callback_query(F.data.in_(["zero_top", "zero_bottom"]))
async def zero_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()

    zero = "top" if callback.data == "zero_top" else "bottom"

    gcode = contour(
        x=data["x"],
        y=data["y"],
        z=data["depth"],
        zero=zero,
        allowance=0
    )

    file = BufferedInputFile(gcode.encode(), filename="contour.nc")

    await callback.message.answer("✅ G-code готов")
    await callback.message.answer_document(file)

    await state.clear()