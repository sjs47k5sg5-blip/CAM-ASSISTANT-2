from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import BufferedInputFile

from services.contour_gcode import contour_gcode
from services.pocket_engine import pocket_gcode

router = Router()

class CAMState(StatesGroup):
    x = State()
    y = State()
    step = State()
    depth = State()
    zero = State()

def safe_float(t):
    try: return float(t)
    except: return None

@router.callback_query(F.data == "cam_contour")
async def start(c: CallbackQuery, s: FSMContext):
    await c.answer()
    await s.clear()
    await c.message.answer("Введите X:")
    await s.set_state(CAMState.x)

@router.message(CAMState.x)
async def x(m: Message, s: FSMContext):
    v = safe_float(m.text)
    if v is None: return await m.answer("ERR")
    await s.update_data(x=v)
    await m.answer("Введите Y:")
    await s.set_state(CAMState.y)

@router.message(CAMState.y)
async def y(m: Message, s: FSMContext):
    v = safe_float(m.text)
    if v is None: return await m.answer("ERR")
    await s.update_data(y=v)
    await m.answer("Шаг (STEP):")
    await s.set_state(CAMState.step)

@router.message(CAMState.step)
async def st(m: Message, s: FSMContext):
    v = safe_float(m.text)
    if v is None: return await m.answer("ERR")
    await s.update_data(step=v)
    await m.answer("Глубина (DEPTH):")
    await s.set_state(CAMState.depth)

@router.message(CAMState.depth)
async def d(m: Message, s: FSMContext):
    v = safe_float(m.text)
    if v is None: return await m.answer("ERR")
    await s.update_data(depth=v)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Верх", callback_data="z_top")],
        [InlineKeyboardButton(text="Низ", callback_data="z_bottom")],
        [InlineKeyboardButton(text="POCKET", callback_data="cam_pocket")]
    ])

    await m.answer("MODE:", reply_markup=kb)
    await s.set_state(CAMState.zero)

@router.callback_query(F.data.in_(["z_top","z_bottom"]))
async def contour(c: CallbackQuery, s: FSMContext):
    await c.answer()
    d = await s.get_data()
    zero = "top" if c.data=="z_top" else "bottom"

    g = contour_gcode(d["x"],d["y"],d["step"],d["depth"],zero)

    file = BufferedInputFile(g.encode(), filename="contour.nc")
    await c.message.answer_document(file, caption="КОНТУР v8")

    await s.clear()

@router.callback_query(F.data == "cam_pocket")
async def pocket(c: CallbackQuery, s: FSMContext):
    await c.answer()
    d = await s.get_data()

    g = pocket_gcode(d["x"], d["y"], d["depth"])
    file = BufferedInputFile(g.encode(), filename="pocket.nc")

    await c.message.answer_document(file, caption="КАРМАН v8")
    await s.clear()
