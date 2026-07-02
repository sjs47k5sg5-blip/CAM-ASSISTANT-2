from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from services.gcode import drilling_gcode

from states import DrillingState

from keyboards.materials import materials_keyboard
from keyboards.drilling import drill_type_keyboard

from services.drilling import (
    get_mode,
    drilling_time,
)

router = Router()


@router.message(F.text == "🕳 Сверление")
async def drilling_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(DrillingState.material)

    await message.answer(
        "🕳 Выберите материал",
        reply_markup=materials_keyboard,
    )


@router.message(DrillingState.material)
async def drilling_material(message: Message, state: FSMContext):
    await state.update_data(material=message.text)

    await state.set_state(DrillingState.tool)

    await message.answer(
        "Выберите тип сверла",
        reply_markup=drill_type_keyboard,
    )


@router.message(DrillingState.tool)
async def drilling_tool(message: Message, state: FSMContext):
    if message.text not in ["HSS", "Твердосплавное"]:
        await message.answer("Выберите тип сверла кнопкой.")
        return

    await state.update_data(tool=message.text)

    await state.set_state(DrillingState.diameter)

    await message.answer("Введите диаметр сверла (мм):")


@router.message(DrillingState.diameter)
async def drilling_diameter(message: Message, state: FSMContext):
    try:
        diameter = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число.")
        return

    await state.update_data(diameter=diameter)

    await state.set_state(DrillingState.depth)

    await message.answer("Введите глубину сверления (мм):")


@router.message(DrillingState.depth)
async def drilling_depth(message: Message, state: FSMContext):
    try:
        depth = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число.")
        return

    data = await state.get_data()

    material = data["material"]
    tool = data["tool"]
    diameter = data["diameter"]

    try:
        mode = get_mode(material, tool, diameter)
    except Exception:
        await message.answer(
            "Для выбранного материала или диаметра нет режимов."
        )
        await state.clear()
        return

    rpm = mode["rpm"]
    feed = mode["feed"]
    cycle = mode["cycle"]
    step = mode["step"]
    coolant = mode["coolant"]

    time_sec = drilling_time(depth, feed)
    gcode = drilling_gcode(
    tool=1,
    rpm=rpm,
    feed=feed,
    depth=depth,
    cycle=cycle,
    step=step,
)

    text = f"""
🕳 СВЕРЛЕНИЕ

Материал:
{material}

Тип сверла:
{tool}

Диаметр:
Ø{diameter:.1f} мм

Глубина:
{depth:.1f} мм

────────────────

Обороты S

{rpm} об/мин

Подача F

{feed} мм/мин

────────────────

Цикл

{cycle}

Шаг вывода

{step} мм

────────────────

Охлаждение

{coolant}

────────────────

Время

≈ {time_sec} сек
"""

    text += f"""

────────────────

Пример G-кода Fanuc

<pre>{gcode}</pre>
"""

    await message.answer(text,     parse_mode="HTML")

    await state.clear() 