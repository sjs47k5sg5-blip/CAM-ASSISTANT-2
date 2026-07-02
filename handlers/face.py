from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import FaceState

from keyboards.materials import materials_keyboard
from keyboards.milling_tools import milling_tools_keyboard
from keyboards.face import face_strategy_keyboard
from keyboards.main_menu import main_menu

from services.material_service import get_modes
from services.face import (
    face_feed,
    face_step,
    face_passes,
    face_time,
)
from services.face_gcode import face_gcode

router = Router()


@router.message(F.text == "🟦 Торцевое фрезерование")
async def face_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(FaceState.material)

    await message.answer(
        "Выберите материал",
        reply_markup=materials_keyboard,
    )


@router.message(FaceState.material)
async def face_material(message: Message, state: FSMContext):

    await state.update_data(material=message.text)

    await state.set_state(FaceState.tool)

    await message.answer(
        "🛠 Выберите тип фрезы",
        reply_markup=milling_tools_keyboard,
    )


@router.message(FaceState.tool)
async def face_tool(message: Message, state: FSMContext):

    tool = message.text

    if tool not in ["Твердосплавная", "HSS"]:
        await message.answer(
            "Выберите тип фрезы кнопкой.",
            reply_markup=milling_tools_keyboard,
        )
        return

    await state.update_data(tool=tool)

    await state.set_state(FaceState.diameter)

    await message.answer("Введите диаметр фрезы (мм):")


@router.message(FaceState.diameter)
async def face_diameter(message: Message, state: FSMContext):

    try:
        diameter = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число.")
        return

    await state.update_data(diameter=diameter)

    await state.set_state(FaceState.teeth)

    await message.answer("Введите количество зубьев:")


@router.message(FaceState.teeth)
async def face_teeth(message: Message, state: FSMContext):

    try:
        teeth = int(message.text)
    except ValueError:
        await message.answer("Введите целое число.")
        return

    await state.update_data(teeth=teeth)

    await state.set_state(FaceState.width)

    await message.answer("Введите ширину обработки (мм):")


@router.message(FaceState.width)
async def face_width(message: Message, state: FSMContext):

    try:
        width = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число.")
        return

    await state.update_data(width=width)

    await state.set_state(FaceState.length)

    await message.answer("Введите длину обработки (мм):")


@router.message(FaceState.length)
async def face_length(message: Message, state: FSMContext):

    try:
        length = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число.")
        return

    await state.update_data(length=length)

    await state.set_state(FaceState.depth)

    await message.answer("Введите глубину обработки (мм):")


@router.message(FaceState.depth)
async def face_depth(message: Message, state: FSMContext):

    try:
        depth = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число.")
        return

    await state.update_data(depth=depth)

    await state.set_state(FaceState.rpm)

    await message.answer("Введите обороты шпинделя S (об/мин):")


@router.message(FaceState.rpm)
async def face_rpm(message: Message, state: FSMContext):

    try:
        rpm = int(message.text)
    except ValueError:
        await message.answer("Введите целое число.")
        return

    await state.update_data(rpm=rpm)

    await state.set_state(FaceState.strategy)

    await message.answer(
        "Выберите стратегию обработки",
        reply_markup=face_strategy_keyboard,
    )


@router.message(FaceState.strategy)
async def face_strategy(message: Message, state: FSMContext):

    strategy = message.text

    data = await state.get_data()

    try:
        modes = get_modes(
            data["material"],
            data["tool"],
        )
    except KeyError:
        await message.answer(
            "Для выбранного материала нет режимов.",
            reply_markup=main_menu,
        )
        await state.clear()
        return

    feed = face_feed(
        data["rpm"],
        data["teeth"],
        modes["fz"],
    )

    step = face_step(
        data["diameter"],
    )

    passes = face_passes(
        data["width"],
        step,
    )

    time_sec = face_time(
        data["length"],
        passes,
        feed,
    )

    gcode = face_gcode(
    tool=1,
    rpm=data["rpm"],
    feed=feed,
    width=data["width"],
    length=data["length"],
    depth=data["depth"],
    step=step,
)
    

    text = f"""
🟦 ТОРЦЕВОЕ ФРЕЗЕРОВАНИЕ

Материал:
{data['material']}

Инструмент:
{data['tool']}

Диаметр:
Ø{data['diameter']:.1f} мм

Количество зубьев:
{data['teeth']}

────────────────

Обороты

S{data['rpm']}

Подача

F{feed}

────────────────

Шаг

{step} мм

Проходов

{passes}

────────────────

Стратегия

{strategy}

────────────────

Время

≈ {time_sec} сек

────────────────

<pre>{gcode}</pre>
"""

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=main_menu,
    )

    await state.clear()