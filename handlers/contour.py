from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import ContourState

from keyboards.contour import contour_keyboard
from keyboards.materials import materials_keyboard
from keyboards.milling_tools import milling_tools_keyboard

router = Router()


@router.message(F.text == "⭕ Контур")
async def contour_start(message: Message, state: FSMContext):

    await state.clear()

    await state.set_state(ContourState.type)

    await message.answer(
        "Выберите тип контура",
        reply_markup=contour_keyboard,
    )


@router.message(ContourState.type)
async def contour_type(message: Message, state: FSMContext):

    contour = message.text

    if contour not in ["⬜ Наружный", "🔲 Внутренний"]:
        await message.answer(
            "Выберите тип контура кнопкой.",
            reply_markup=contour_keyboard,
        )
        return

    await state.update_data(type=contour)

    await state.set_state(ContourState.material)

    await message.answer(
        "Выберите материал",
        reply_markup=materials_keyboard,
    )


@router.message(ContourState.material)
async def contour_material(message: Message, state: FSMContext):

    await state.update_data(material=message.text)

    await state.set_state(ContourState.tool)

    await message.answer(
        "Выберите тип фрезы",
        reply_markup=milling_tools_keyboard,
    )


@router.message(ContourState.tool)
async def contour_tool(message: Message, state: FSMContext):

    tool = message.text

    if tool not in ["Твердосплавная", "HSS"]:
        await message.answer(
            "Выберите инструмент кнопкой.",
            reply_markup=milling_tools_keyboard,
        )
        return

    await state.update_data(tool=tool)

    await state.set_state(ContourState.diameter)

    await message.answer(
        "Введите диаметр фрезы (мм):"
    )