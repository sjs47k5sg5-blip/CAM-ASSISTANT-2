from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from services.contour import generate_gcode

router = Router()

class CAM(StatesGroup):
    x = State()
    y = State()
    step = State()
    depth = State()

@router.message(F.text == "Контур")
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Введите X:")
    await state.set_state(CAM.x)

@router.message(CAM.x)
async def x(message: Message, state: FSMContext):
    await state.update_data(x=float(message.text))
    await message.answer("Введите Y:")
    await state.set_state(CAM.y)

@router.message(CAM.y)
async def y(message: Message, state: FSMContext):
    await state.update_data(y=float(message.text))
    await message.answer("Шаг:")
    await state.set_state(CAM.step)

@router.message(CAM.step)
async def step(message: Message, state: FSMContext):
    await state.update_data(step=float(message.text))
    await message.answer("Глубина:")
    await state.set_state(CAM.depth)

@router.message(CAM.depth)
async def depth(message: Message, state: FSMContext):
    data = await state.get_data()
    depth = float(message.text)

    gcode = generate_gcode(
        x=data["x"],
        y=data["y"],
        step=data["step"],
        depth=depth
    )

    file = BufferedInputFile(gcode.encode(), filename="contour.nc")

    await message.answer_document(file)
    await state.clear()