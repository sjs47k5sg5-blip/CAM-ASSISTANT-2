from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from services.cam_engine import contour

router = Router()

class CAM(StatesGroup):
    tool = State()
    zero = State()
    x = State()
    y = State()
    depth = State()
    stepdown = State()
    allowance = State()
    corner_type = State()
    corner_value = State()
    zone = State()

# START
@router.message(F.text == "📐 Контур")
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Диаметр инструмента:")
    await state.set_state(CAM.tool)

# TOOL
@router.message(CAM.tool)
async def tool(message: Message, state: FSMContext):
    await state.update_data(tool=float(message.text))
    await message.answer("X0 Y0 Z0 (введите OK)")
    await state.set_state(CAM.zero)

# ZERO
@router.message(CAM.zero)
async def zero(message: Message, state: FSMContext):
    await message.answer("Введите X:")
    await state.set_state(CAM.x)

# X
@router.message(CAM.x)
async def x(message: Message, state: FSMContext):
    await state.update_data(x=float(message.text))
    await message.answer("Y:")
    await state.set_state(CAM.y)

# Y
@router.message(CAM.y)
async def y(message: Message, state: FSMContext):
    await state.update_data(y=float(message.text))
    await message.answer("Глубина:")
    await state.set_state(CAM.depth)

# DEPTH
@router.message(CAM.depth)
async def depth(message: Message, state: FSMContext):
    await state.update_data(depth=float(message.text))
    await message.answer("Шаг по глубине:")
    await state.set_state(CAM.stepdown)

# STEPDOWN
@router.message(CAM.stepdown)
async def stepdown(message: Message, state: FSMContext):
    await state.update_data(stepdown=float(message.text))
    await message.answer("Припуск (0 если нет):")
    await state.set_state(CAM.allowance)

# ALLOWANCE
@router.message(CAM.allowance)
async def allowance(message: Message, state: FSMContext):
    await state.update_data(allowance=float(message.text))
    await message.answer("Углы: FASKA / RADIUS / NONE")
    await state.set_state(CAM.corner_type)

# CORNER TYPE
@router.message(CAM.corner_type)
async def corner_type(message: Message, state: FSMContext):
    await state.update_data(corner_type=message.text)

    if message.text in ["FASKA", "RADIUS"]:
        await message.answer("Введите значение:")
        await state.set_state(CAM.corner_value)
    else:
        await state.update_data(corner_value=0)
        await message.answer("Зона: ALL / TL / TR / BL / BR")
        await state.set_state(CAM.zone)

# CORNER VALUE
@router.message(CAM.corner_value)
async def corner_value(message: Message, state: FSMContext):
    await state.update_data(corner_value=float(message.text))
    await message.answer("Зона: ALL / TL / TR / BL / BR")
    await state.set_state(CAM.zone)

# ZONE + BUILD
@router.message(CAM.zone)
async def zone(message: Message, state: FSMContext):
    data = await state.get_data()

    gcode = contour(
        data["x"],
        data["y"],
        data["depth"],
        data["stepdown"],
        data["tool"],
        data["allowance"],
        data["stepdown"],
        data["corner_type"],
        data["corner_value"],
        message.text
    )

    file = BufferedInputFile(gcode.encode(), filename="cam.nc")
    await message.answer_document(file)

    await state.clear()
