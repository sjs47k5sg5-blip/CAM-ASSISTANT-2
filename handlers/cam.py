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

@router.message(F.text == "📐 Контур")
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("X:")
    await state.set_state(CAM.x)

@router.message(CAM.x)
async def x(message: Message, state: FSMContext):
    await state.update_data(x=message.text)
    await message.answer("Y:")
    await state.set_state(CAM.y)

@router.message(CAM.y)
async def y(message: Message, state: FSMContext):
    await state.update_data(y=message.text)
    await message.answer("STEP:")
    await state.set_state(CAM.step)

@router.message(CAM.step)
async def step(message: Message, state: FSMContext):
    await state.update_data(step=message.text)
    await message.answer("DEPTH:")
    await state.set_state(CAM.depth)

@router.message(CAM.depth)
async def depth(message: Message, state: FSMContext):
    data = await state.get_data()

    gcode = f"""G21
G90
G1 X{data['x']} Y{data['y']}
G1 Z-{message.text}
M30"""

    file = BufferedInputFile(gcode.encode(), filename="cam.nc")
    await message.answer_document(file)
    await state.clear()
