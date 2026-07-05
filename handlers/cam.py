from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from services.gcode import contour
from services.engine import build_plan

router = Router()

class S(StatesGroup):
    x=State()
    y=State()
    z=State()
    allowance=State()
    feature=State()
    tool=State()
    zero=State()

def num(t):
    try: return float(t)
    except: return None

@router.message(F.text == "📐 CAM")
async def start(m: Message, s: FSMContext):
    await m.answer("X:")
    await s.set_state(S.x)

@router.message(S.x)
async def x(m: Message, s: FSMContext):
    v=num(m.text)
    if v is None: return await m.answer("err")
    await s.update_data(x=v)
    await m.answer("Y:")
    await s.set_state(S.y)

@router.message(S.y)
async def y(m: Message, s: FSMContext):
    v=num(m.text)
    if v is None: return await m.answer("err")
    await s.update_data(y=v)
    await m.answer("Z:")
    await s.set_state(S.z)

@router.message(S.z)
async def z(m: Message, s: FSMContext):
    v=num(m.text)
    if v is None: return await m.answer("err")
    await s.update_data(z=v)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ОСТРЫЕ", callback_data="f_sharp")],
        [InlineKeyboardButton(text="ФАСКА", callback_data="f_chamfer")],
        [InlineKeyboardButton(text="РАДИУС", callback_data="f_radius")]
    ])

    await m.answer("FEATURE:", reply_markup=kb)
    await s.set_state(S.feature)

@router.callback_query(F.data.startswith("f_"))
async def feature(c: CallbackQuery, s: FSMContext):
    await c.answer()
    await s.update_data(feature=c.data)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 инструмент", callback_data="t1")],
        [InlineKeyboardButton(text="Черновой+Чистовой", callback_data="t2")]
    ])

    await c.message.answer("TOOL MODE:", reply_markup=kb)
    await s.set_state(S.tool)

@router.callback_query(F.data.in_(["t1","t2"]))
async def tool(c: CallbackQuery, s: FSMContext):
    await c.answer()
    await s.update_data(tool=c.data)

    await c.message.answer("Припуск:")
    await s.set_state(S.allowance)

@router.message(S.allowance)
async def allowance(m: Message, s: FSMContext):
    v=num(m.text)
    if v is None: return await m.answer("err")
    await s.update_data(allowance=v)

    data = await s.get_data()
    plan = build_plan(data)

    gcode = contour(data["x"],data["y"],data["z"],"top",data["allowance"])

    file = BufferedInputFile(gcode.encode(), filename="FULL_CAM.nc")
    await m.answer_document(file, caption="FULL CAM READY")

    await s.clear()
