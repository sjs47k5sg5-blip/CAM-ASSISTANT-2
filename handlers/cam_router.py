
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from services.contour_gcode import contour_gcode

router = Router()

class CAMState(StatesGroup):
    w = State()
    h = State()
    step = State()
    depth = State()
    zero = State()

# START CAM FLOW
@router.callback_query(F.data == "cam_contour")
async def start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    await callback.message.answer("Введите X:")
    await state.set_state(CAMState.w)

@router.message(CAMState.w)
async def w(m: Message, s: FSMContext):
    await s.update_data(w=float(m.text))
    await m.answer("Введите Y:")
    await s.set_state(CAMState.h)

@router.message(CAMState.h)
async def h(m: Message, s: FSMContext):
    await s.update_data(h=float(m.text))
    await m.answer("Шаг по глубине:")
    await s.set_state(CAMState.step)

@router.message(CAMState.step)
async def st(m: Message, s: FSMContext):
    await s.update_data(step=float(m.text))
    await m.answer("Глубина:")
    await s.set_state(CAMState.depth)

@router.message(CAMState.depth)
async def d(m: Message, s: FSMContext):
    await s.update_data(depth=float(m.text))

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬆️ Верх", callback_data="z_top")],
        [InlineKeyboardButton(text="⬇️ Низ", callback_data="z_bottom")]
    ])

    await m.answer("Выбор нуля:", reply_markup=kb)
    await s.set_state(CAMState.zero)

@router.callback_query(F.data.in_(["z_top","z_bottom"]))
async def zero(c: CallbackQuery, s: FSMContext):
    await c.answer()
    data = await s.get_data()

    zero_mode = "top" if c.data == "z_top" else "bottom"

    gcode = contour_gcode(
        data["w"],
        data["h"],
        data["step"],
        data["depth"],
        zero_mode
    )

    await c.message.answer_document(gcode.encode())
    await s.clear()
