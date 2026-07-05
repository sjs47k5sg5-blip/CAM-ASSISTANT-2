from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from services.cam_engine import contour
from keyboards.cam_menu import zero_kb

router = Router()

class CAM(StatesGroup):
    tool = State()
    zero = State()
    size_x = State()
    size_y = State()
    depth = State()
    feed = State()

@router.message(F.text == "📐 Контур")
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Диаметр инструмента:")
    await state.set_state(CAM.tool)

@router.message(CAM.tool)
async def tool(message: Message, state: FSMContext):
    await state.update_data(tool=int(message.text))
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
    await message.answer("X размер:")
    await state.set_state(CAM.size_x)

@router.message(CAM.size_x)
async def sx(message: Message, state: FSMContext):
    await state.update_data(sx=float(message.text))
    await message.answer("Y размер:")
    await state.set_state(CAM.size_y)

@router.message(CAM.size_y)
async def sy(message: Message, state: FSMContext):
    await state.update_data(sy=float(message.text))
    await message.answer("Глубина:")
    await state.set_state(CAM.depth)

@router.message(CAM.depth)
async def depth(message: Message, state: FSMContext):
    await state.update_data(depth=float(message.text))
    await message.answer("Подача:")
    await state.set_state(CAM.feed)

@router.message(CAM.feed)
async def feed(message: Message, state: FSMContext):
    data = await state.get_data()

    gcode = contour(
        data["sx"], data["sy"],
        data["depth"], float(message.text),
        data["tool"],
        data["zero"],
        data["sx"], data["sy"]
    )

    file = BufferedInputFile(gcode.encode(), filename="cam.nc")
    await message.answer_document(file)

    await state.clear()
