from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from services.cam_engine import contour
from keyboards.cam_menu import zero_kb, corner_kb, corner_zone_kb

router = Router()


# =========================
# FSM STATES
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

    corner_zone = State()


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
    await state.update_data(tool=float(message.text))
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

    await message.answer("X размер:")
    await state.set_state(CAM.x)


# =========================
# X
# =========================
@router.message(CAM.x)
async def x(message: Message, state: FSMContext):
    await state.update_data(x=float(message.text))
    await message.answer("Y размер:")
    await state.set_state(CAM.y)


# =========================
# Y
# =========================
@router.message(CAM.y)
async def y(message: Message, state: FSMContext):
    await state.update_data(y=float(message.text))
    await message.answer("Глубина:")
    await state.set_state(CAM.depth)


# =========================
# DEPTH
# =========================
@router.message(CAM.depth)
async def depth(message: Message, state: FSMContext):
    await state.update_data(depth=float(message.text))
    await message.answer("Шаг по глубине:")
    await state.set_state(CAM.stepdown)


# =========================
# STEPDOWN
# =========================
@router.message(CAM.stepdown)
async def stepdown(message: Message, state: FSMContext):
    await state.update_data(stepdown=float(message.text))
    await message.answer("Припуск (0 если нет):")
    await state.set_state(CAM.allowance)


# =========================
# ALLOWANCE
# =========================
@router.message(CAM.allowance)
async def allowance(message: Message, state: FSMContext):
    await state.update_data(allowance=float(message.text))

    await message.answer("Углы обработки:", reply_markup=corner_kb())
    await state.set_state(CAM.corner)


# =========================
# CORNER TYPE
# =========================
@router.message(CAM.corner)
async def corner(message: Message, state: FSMContext):

    await state.update_data(corner_type=message.text)

    # 💥 FIX: теперь есть ввод значения
    if message.text in ["ФАСКА", "РАДИУС"]:
        await message.answer("Введите размер (мм):")
        await state.set_state(CAM.corner_value)
        return

    await message.answer("Выберите зоны:", reply_markup=corner_zone_kb())
    await state.set_state(CAM.corner_zone)


# =========================
# CORNER VALUE (FIXED)
# =========================
@router.message(CAM.corner_value)
async def corner_value(message: Message, state: FSMContext):

    try:
        value = float(message.text)
    except:
        return await message.answer("Введите число (например 0.5)")

    await state.update_data(corner_value=value)

    await message.answer("Выберите зоны:", reply_markup=corner_zone_kb())
    await state.set_state(CAM.corner_zone)


# =========================
# FINAL STEP
# =========================
@router.message(CAM.corner_zone)
async def corner_zone(message: Message, state: FSMContext):

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
    )

    file = BufferedInputFile(gcode.encode(), filename="cam.nc")

    await message.answer_document(file)

    await state.clear()