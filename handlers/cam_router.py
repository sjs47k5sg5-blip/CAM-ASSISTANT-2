from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import BufferedInputFile

from services.contour_gcode import contour_gcode

router = Router()


class CAMState(StatesGroup):
    x = State()
    y = State()
    step = State()
    depth = State()
    zero = State()


def safe_float(text: str):
    try:
        return float(text)
    except:
        return None


# =========================
# START
# =========================
@router.callback_query(F.data == "cam_contour")
async def start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    await callback.message.answer("📐 Введите X:")
    await state.set_state(CAMState.x)


# =========================
# X
# =========================
@router.message(CAMState.x)
async def x(message: Message, state: FSMContext):
    val = safe_float(message.text)
    if val is None:
        return await message.answer("❌ Введите число")

    await state.update_data(x=val)
    await message.answer("📏 Введите Y:")
    await state.set_state(CAMState.y)


# =========================
# Y
# =========================
@router.message(CAMState.y)
async def y(message: Message, state: FSMContext):
    val = safe_float(message.text)
    if val is None:
        return await message.answer("❌ Введите число")

    await state.update_data(y=val)
    await message.answer("📉 STEP:")
    await state.set_state(CAMState.step)


# =========================
# STEP
# =========================
@router.message(CAMState.step)
async def step(message: Message, state: FSMContext):
    val = safe_float(message.text)
    if val is None:
        return await message.answer("❌ Введите число")

    await state.update_data(step=val)
    await message.answer("📦 DEPTH:")
    await state.set_state(CAMState.depth)


# =========================
# DEPTH
# =========================
@router.message(CAMState.depth)
async def depth(message: Message, state: FSMContext):
    val = safe_float(message.text)
    if val is None:
        return await message.answer("❌ Введите число")

    await state.update_data(depth=val)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬆️ TOP", callback_data="z_top")],
        [InlineKeyboardButton(text="⬇️ BOTTOM", callback_data="z_bottom")]
    ])

    await message.answer("📍 Выберите ноль:", reply_markup=kb)
    await state.set_state(CAMState.zero)


# =========================
# GENERATE + EXPORT FILE (FIX)
# =========================
@router.callback_query(F.data.in_(["z_top", "z_bottom"]))
async def zero(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    zero_mode = "top" if callback.data == "z_top" else "bottom"

    gcode = contour_gcode(
        data["x"],
        data["y"],
        data["step"],
        data["depth"],
        zero_mode
    )

    # 🔥 ВАЖНЫЙ ФИКС: реальный файл Telegram
    file = BufferedInputFile(
        gcode.encode("utf-8"),
        filename="contour.nc"
    )

    await callback.message.answer("✅ G-code готов")

    await callback.message.answer_document(
        document=file,
        caption="CAM EXPORT READY"
    )

    await state.clear() 