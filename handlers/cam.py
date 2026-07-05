from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

# 🔥 FIX: правильный импорт под любой cam_engine
from services.cam_engine import generate_toolpath as contour

from keyboards.cam_menu import zero_kb, corner_kb, allowance_kb

router = Router()


# =========================
# FSM
# =========================
class CAM(StatesGroup):
    tool = State()
    zero = State()

    x = State()
    y = State()

    depth = State()
    stepdown = State()

    allowance = State()

    corner = State()
    corner_value = State()


# =========================
# START
# =========================
@router.message(F.text == "📐 Контур")
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Диаметр инструмента:")
    await state.set_state(CAM.tool)


# =========================
# TOOL
# =========================
@router.message(CAM.tool)
async def tool(message: Message, state: FSMContext):

    try:
        tool = float(message.text)
    except:
        return await message.answer("Введите число (например 10)")

    await state.update_data(tool=tool)

    await message.answer("Выбор нуля:", reply_markup=zero_kb())
    await state.set_state(CAM.zero)


# =========================
# ZERO
# =========================
@router.message(CAM.zero)
async def zero(message: Message, state: FSMContext):

    zmap = {
        "📍 Центр детали": "CENTER",
        "📍 ЛВ угол": "TL",
        "📍 ПВ угол": "TR",
        "📍 ЛН угол": "BL",
        "📍 ПН угол": "BR",
    }

    await state.update_data(zero=zmap.get(message.text, "CENTER"))

    await message.answer("X:")
    await state.set_state(CAM.x)


# =========================
# X
# =========================
@router.message(CAM.x)
async def x(message: Message, state: FSMContext):

    await state.update_data(x=float(message.text))
    await message.answer("Y:")
    await state.set_state(CAM.y)


# =========================
# Y
# =========================
@router.message(CAM.y)
async def y(message: Message, state: FSMContext):

    await state.update_data(y=float(message.text))
    await message.answer("Depth:")
    await state.set_state(CAM.depth)


# =========================
# DEPTH
# =========================
@router.message(CAM.depth)
async def depth(message: Message, state: FSMContext):

    await state.update_data(depth=float(message.text))
    await message.answer("Stepdown:")
    await state.set_state(CAM.stepdown)


# =========================
# STEPDOWN
# =========================
@router.message(CAM.stepdown)
async def stepdown(message: Message, state: FSMContext):

    await state.update_data(stepdown=float(message.text))

    await message.answer("Allowance:", reply_markup=allowance_kb())
    await state.set_state(CAM.allowance)


# =========================
# ALLOWANCE
# =========================
@router.message(CAM.allowance)
async def allowance(message: Message, state: FSMContext):

    map_allow = {
        "0 mm": 0.0,
        "0.1 mm": 0.1,
        "0.2 mm": 0.2,
        "0.5 mm": 0.5,
        "1.0 mm": 1.0
    }

    value = map_allow.get(message.text)

    if value is None:
        return await message.answer("Выберите кнопками")

    await state.update_data(allowance=value)

    await message.answer("Corner type:", reply_markup=corner_kb())
    await state.set_state(CAM.corner)


# =========================
# CORNER
# =========================
@router.message(CAM.corner)
async def corner(message: Message, state: FSMContext):

    await state.update_data(corner_type=message.text)

    if message.text in ["ФАСКА", "РАДИУС"]:
        await message.answer("Введите размер (мм):")
        await state.set_state(CAM.corner_value)
        return

    await state.update_data(corner_value=0)
    await build(message, state)


# =========================
# CORNER VALUE
# =========================
@router.message(CAM.corner_value)
async def corner_value(message: Message, state: FSMContext):

    try:
        await state.update_data(corner_value=float(message.text))
    except:
        return await message.answer("Введите число")

    await build(message, state)


# =========================
# BUILD
# =========================
async def build(message: Message, state: FSMContext):

    data = await state.get_data()

    gcode = contour(
        data["x"],
        data["y"],
        data["depth"],
        data["stepdown"],
        data["tool"],
        data["zero"],
        data["allowance"],
        data["stepdown"],
        data["corner_type"],
        data["corner_value"]
    )

    file = BufferedInputFile(gcode.encode(), filename="cam.nc")

    await message.answer_document(file)

    await state.clear()