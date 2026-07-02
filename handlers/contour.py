from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from states import ContourState

from keyboards.contour import contour_keyboard
from keyboards.materials import materials_keyboard
from keyboards.milling_tools import milling_tools_keyboard
from keyboards.allowance import allowance_keyboard
from keyboards.direction import direction_keyboard
from keyboards.main_menu import main_menu

from services.material_service import get_modes
from services.contour import (
    contour_feed,
    contour_passes,
    contour_time,
)
from services.contour_gcode import contour_gcode

router = Router()


@router.message(F.text == "⭕ Контур")
async def contour_start(message: Message, state: FSMContext):

    await state.clear()

    await state.set_state(ContourState.type)

    await message.answer(
        "⭕ Выберите тип контура",
        reply_markup=contour_keyboard,
    )


@router.message(ContourState.type)
async def contour_type(message: Message, state: FSMContext):

    if message.text not in ("⬜ Наружный", "🔲 Внутренний"):
        await message.answer(
            "Выберите вариант кнопкой.",
            reply_markup=contour_keyboard,
        )
        return

    await state.update_data(
        side=message.text
    )

    await state.set_state(
        ContourState.material
    )

    await message.answer(
        "Выберите материал",
        reply_markup=materials_keyboard,
    )


@router.message(ContourState.material)
async def contour_material(message: Message, state: FSMContext):

    await state.update_data(
        material=message.text
    )

    await state.set_state(
        ContourState.tool
    )

    await message.answer(
        "Выберите инструмент",
        reply_markup=milling_tools_keyboard,
    )


@router.message(ContourState.tool)
async def contour_tool(message: Message, state: FSMContext):

    await state.update_data(
        tool=message.text
    )

    await state.set_state(
        ContourState.diameter
    )

    await message.answer(
        "Введите диаметр фрезы (мм):"
    )
@router.message(ContourState.diameter)
async def contour_diameter(message: Message, state: FSMContext):

    try:
        diameter = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число.")
        return

    await state.update_data(diameter=diameter)

    await state.set_state(ContourState.teeth)

    await message.answer(
        "Введите количество зубьев:"
    )


@router.message(ContourState.teeth)
async def contour_teeth(message: Message, state: FSMContext):

    try:
        teeth = int(message.text)
    except ValueError:
        await message.answer("Введите целое число.")
        return

    await state.update_data(teeth=teeth)

    await state.set_state(ContourState.length)

    await message.answer(
        "Введите размер по X (мм):"
    )


@router.message(ContourState.length)
async def contour_length(message: Message, state: FSMContext):

    try:
        length = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число.")
        return

    await state.update_data(length=length)

    await state.set_state(ContourState.width)

    await message.answer(
        "Введите размер по Y (мм):"
    )


@router.message(ContourState.width)
async def contour_width(message: Message, state: FSMContext):

    try:
        width = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число.")
        return

    await state.update_data(width=width)

    await state.set_state(ContourState.depth)

    await message.answer(
        "Введите глубину обработки Z (мм):"
    )


@router.message(ContourState.depth)
async def contour_depth(message: Message, state: FSMContext):

    try:
        depth = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число.")
        return

    await state.update_data(depth=depth)

    await state.set_state(ContourState.step)

    await message.answer(
        "Введите шаг по Z (Ap, мм):"
    )


@router.message(ContourState.step)
async def contour_step(message: Message, state: FSMContext):

    try:
        step = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число.")
        return

    await state.update_data(step=step)

    await state.set_state(ContourState.rpm)

    await message.answer(
        "Введите обороты шпинделя S (об/мин):"
    )
@router.message(ContourState.rpm)
async def contour_rpm(message: Message, state: FSMContext):

    try:
        rpm = int(message.text)
    except ValueError:
        await message.answer("Введите целое число.")
        return

    await state.update_data(rpm=rpm)

    await state.set_state(ContourState.allowance)

    await message.answer(
        "Выберите припуск (мм):",
        reply_markup=allowance_keyboard,
    )


@router.message(ContourState.allowance)
async def contour_allowance(message: Message, state: FSMContext):

    try:
        allowance = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer(
            "Выберите припуск кнопкой.",
            reply_markup=allowance_keyboard,
        )
        return

    await state.update_data(allowance=allowance)

    await state.set_state(ContourState.direction)

    await message.answer(
        "Выберите направление фрезерования",
        reply_markup=direction_keyboard,
    )
@router.message(ContourState.direction)
async def contour_direction(message: Message, state: FSMContext):

    direction = message.text

    data = await state.get_data()

    try:
        modes = get_modes(
            data["material"],
            data["tool"],
        )
    except KeyError:
        await message.answer(
            "❌ Для выбранного материала или инструмента нет режимов.",
            reply_markup=main_menu,
        )
        await state.clear()
        return

    feed = contour_feed(
        data["rpm"],
        data["teeth"],
        modes["fz"],
    )

    passes = contour_passes(
        data["depth"],
        data["step"],
    )

    time_sec = contour_time(
        data["length"],
        data["width"],
        passes,
        feed,
    )

    outside = data["side"] == "⬜ Наружный"
    climb = direction == "➡️ Попутное"

    gcode = contour_gcode(
        tool=1,
        rpm=data["rpm"],
        feed=feed,
        diameter=data["diameter"],
        length=data["length"],
        width=data["width"],
        depth=data["depth"],
        step=data["step"],
        allowance=data["allowance"],
        outside=outside,
        climb=climb,
    )

    filename = "CONTOUR.nc"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(gcode)

    await message.answer(
        f"""
⭕ КОНТУР

Тип:
{data["side"]}

Материал:
{data["material"]}

Инструмент:
{data["tool"]}

Диаметр:
Ø{data["diameter"]:.1f} мм

Количество зубьев:
{data["teeth"]}

────────────────

Обороты

S{data["rpm"]}

Подача

F{feed}

────────────────

Глубина

{data["depth"]} мм

Шаг по Z

{data["step"]} мм

Проходов

{passes}

────────────────

Припуск

{data["allowance"]} мм

────────────────

Время обработки

≈ {time_sec} сек

────────────────

<pre>{gcode}</pre>
""",
        parse_mode="HTML",
        reply_markup=main_menu,
    )

    await message.answer_document(
        FSInputFile(filename),
        caption="📄 CONTOUR.nc",
    )

    await state.clear()