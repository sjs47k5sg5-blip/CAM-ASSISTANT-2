from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from services.cam_engine import generate_gcode

router = Router()

class CAM(StatesGroup):
    x = State()
    y = State()
    depth = State()
    tool = State()
    mode = State()

@router.message(F.text == "📐 Контур")
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("X:")
    await state.set_state(CAM.x)

@router.message(CAM.x)
async def x(message: Message, state: FSMContext):
    await state.update_data(x=float(message.text))
    await message.answer("Y:")
    await state.set_state(CAM.y)

@router.message(CAM.y)
async def y(message: Message, state: FSMContext):
    await state.update_data(y=float(message.text))
    await message.answer("DEPTH:")
    await state.set_state(CAM.depth)

@router.message(CAM.depth)
async def depth(message: Message, state: FSMContext):
    await state.update_data(depth=float(message.text))
    await message.answer("TOOL (1-3):")
    await state.set_state(CAM.tool)

@router.message(CAM.tool)
async def tool(message: Message, state: FSMContext):
    await state.update_data(tool=int(message.text))
    await message.answer("MODE (contour/pocket):")
    await state.set_state(CAM.mode)

@router.message(CAM.mode)
async def mode(message: Message, state: FSMContext):
    data = await state.get_data()

    gcode = generate_gcode(
        data["x"], data["y"], data["depth"], data["tool"], message.text
    )

    file = BufferedInputFile(gcode.encode(), filename="cam.nc")
    await message.answer_document(file)

    await state.clear()
