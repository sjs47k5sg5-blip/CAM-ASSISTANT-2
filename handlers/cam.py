from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from services.cam_engine import generate_toolpath
from keyboards.cam_menu import zero_kb, corner_kb

router = Router()


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


@router.message(F.text == "📐 Контур")
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Диаметр инструмента:")
    await state.set_state(CAM.tool)


@router.message(CAM.tool)
async def tool(message: Message, state: FSMContext):
    await state.update_data(tool=float(message.text))
    await message.answer("Выбор нуля:", reply_markup=zero_kb())
    await state.set_state(CAM.zero)


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


@router.message(CAM.x)
async def x(message: Message, state: FSMContext):
    await state.update_data(x=float(message.text))
    await message.answer("Y:")
    await state.set_state(CAM.y)


@router.message(CAM.y)
async def y(message: Message, state: FSMContext):
    await state.update_data(y=float(message.text))
    await message.answer("Depth:")
    await state.set_state(CAM.depth)


@router.message(CAM.depth)
async def depth(message: Message, state: FSMContext):
    await state.update_data(depth=float(message.text))
    await message.answer("Stepdown:")
    await state.set_state(CAM.stepdown)


@router.message(CAM.stepdown)
async def stepdown(message: Message, state: FSMContext):
    await state.update_data(stepdown=float(message.text))
    await message.answer("Allowance (0 if none):")
    await state.set_state(CAM.allowance)


@router.message(CAM.allowance)
async def allowance(message: Message, state: FSMContext):
    await state.update_data(allowance=float(message.text))
    await message.answer("Corner type: ФАСКА / РАДИУС / ОСТРЫЕ")
    await state.set_state(CAM.corner)


@router.message(CAM.corner)
async def corner(message: Message, state: FSMContext):

    await state.update_data(corner_type=message.text)

    if message.text in ["ФАСКА", "РАДИУС"]:
        await message.answer("Corner size (mm):")
        await state.set_state(CAM.corner_value)
        return

    await state.update_data(corner_value=0)
    await build(message, state)


@router.message(CAM.corner_value)
async def corner_value(message: Message, state: FSMContext):

    await state.update_data(corner_value=float(message.text))
    await build(message, state)


async def build(message: Message, state: FSMContext):

    data = await state.get_data()

    gcode = generate_toolpath(
        data["x"],
        data["y"],
        data["depth"],
        data["stepdown"],
        data["tool"],
        data["zero"],
        data["allowance"],
        data["corner_type"],
        data["corner_value"]
    )

    file = BufferedInputFile(gcode.encode(), filename="cam.nc")
    await message.answer_document(file)

    await state.clear()