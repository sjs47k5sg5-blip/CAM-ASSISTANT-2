from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from services.contour_gcode import contour_gcode

router = Router()

class CAMState(StatesGroup):
    x = State()
    y = State()
    step = State()
    depth = State()
    zero = State()

@router.callback_query(F.data == "cam_contour")
async def start(c: CallbackQuery, state: FSMContext):
    await c.answer()
    await state.clear()
    await c.message.answer("X:")
    await state.set_state(CAMState.x)

@router.message(CAMState.x)
async def x(m: Message, s: FSMContext):
    await s.update_data(x=float(m.text))
    await m.answer("Y:")
    await s.set_state(CAMState.y)

@router.message(CAMState.y)
async def y(m: Message, s: FSMContext):
    await s.update_data(y=float(m.text))
    await m.answer("STEP:")
    await s.set_state(CAMState.step)

@router.message(CAMState.step)
async def step(m: Message, s: FSMContext):
    await s.update_data(step=float(m.text))
    await m.answer("DEPTH:")
    await s.set_state(CAMState.depth)

@router.message(CAMState.depth)
async def depth(m: Message, s: FSMContext):
    await s.update_data(depth=float(m.text))

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬆️ TOP", callback_data="z_top")],
        [InlineKeyboardButton(text="⬇️ BOTTOM", callback_data="z_bottom")]
    ])

    await m.answer("ZERO MODE:", reply_markup=kb)
    await s.set_state(CAMState.zero)

@router.callback_query(F.data.in_(["z_top","z_bottom"]))
async def zero(c: CallbackQuery, s: FSMContext):
    await c.answer()
    data = await s.get_data()

    zero = "top" if c.data == "z_top" else "bottom"

    gcode = contour_gcode(data["x"], data["y"], data["step"], data["depth"], zero)

    await c.message.answer_document(gcode.encode(), caption="CAM V7 PRO")
    await s.clear()
