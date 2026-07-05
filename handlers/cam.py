from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()


class CAM(StatesGroup):
    x = State()
    y = State()
    step = State()
    depth = State()


# =========================
# START CAM
# =========================
@router.message(F.text == "Контур")
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Введите X:")
    await state.set_state(CAM.x)


# =========================
# X
# =========================
@router.message(CAM.x)
async def x_step(message: Message, state: FSMContext):
    try:
        x = float(message.text)
    except:
        return await message.answer("❌ Введите число X")

    await state.update_data(x=x)
    await message.answer("Введите Y:")
    await state.set_state(CAM.y)


# =========================
# Y
# =========================
@router.message(CAM.y)
async def y_step(message: Message, state: FSMContext):
    try:
        y = float(message.text)
    except:
        return await message.answer("❌ Введите число Y")

    await state.update_data(y=y)
    await message.answer("Шаг:")
    await state.set_state(CAM.step)


# =========================
# STEP
# =========================
@router.message(CAM.step)
async def step(message: Message, state: FSMContext):
    try:
        s = float(message.text)
    except:
        return await message.answer("❌ Введите шаг")

    await state.update_data(step=s)
    await message.answer("Глубина:")
    await state.set_state(CAM.depth)


# =========================
# DEPTH → GCODE
# =========================
@router.message(CAM.depth)
async def depth(message: Message, state: FSMContext):
    try:
        d = float(message.text)
    except:
        return await message.answer("❌ Введите глубину")

    data = await state.get_data()

    gcode = f"""
%
O1001
G21
G90

X{data['x']} Y{data['y']}
STEP {data['step']}
DEPTH {d}

G0 Z5
G1 Z-{d} F100

G1 X{data['x']}
G1 Y{data['y']}
G1 X0 Y0

G0 Z5
M30
%
"""

    file = BufferedInputFile(gcode.encode(), filename="contour.nc")

    await message.answer_document(file)
    await state.clear()