from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import DrillingState

from services.drilling import (
    spindle_speed,
    feed_rate,
    get_cutting_data,
    drilling_cycle,
    drilling_time,
    coolant,
)

router = Router()


DRILL_TYPES = [
    "HSS",
    "Твердосплавное",
]


@router.message(F.text == "🕳 Сверление")
async def drilling_start(message: Message, state: FSMContext):

    await state.clear()

    await state.set_state(DrillingState.material)

    await message.answer(
        "Введите материал\n\nНапример:\nСталь 45"
    )


@router.message(DrillingState.material)
async def drilling_material(message: Message, state: FSMContext):

    await state.update_data(material=message.text)

    await state.set_state(DrillingState.tool)

    await message.answer(
        "Введите тип сверла:\n\nHSS\nили\nТвердосплавное"
    )


@router.message(DrillingState.tool)
async def drilling_tool(message: Message, state: FSMContext):

    if message.text not in DRILL_TYPES:

        await message.answer(
            "Введите HSS или Твердосплавное"
        )

        return

    await state.update_data(tool=message.text)

    await state.set_state(DrillingState.diameter)

    await message.answer(
        "Введите диаметр сверла (мм)"
    )


@router.message(DrillingState.diameter)
async def drilling_diameter(message: Message, state: FSMContext):

    try:
        diameter = float(message.text.replace(",", "."))

    except ValueError:

        await message.answer("Введите число.")

        return

    await state.update_data(diameter=diameter)

    await state.set_state(DrillingState.depth)

    await message.answer(
        "Введите глубину сверления (мм)"
    )


@router.message(DrillingState.depth)
async def drilling_result(message: Message, state: FSMContext):

    try:
        depth = float(message.text.replace(",", "."))

    except ValueError:

        await message.answer("Введите число.")

        return

    data = await state.get_data()

    material = data["material"]
    tool = data["tool"]
    diameter = data["diameter"]

    vc, fn = get_cutting_data(
        material,
        tool,
        diameter,
    )

    rpm = spindle_speed(vc, diameter)

    feed = feed_rate(rpm, fn)

    cycle, step = drilling_cycle(
        depth,
        diameter,
    )

    time_sec = drilling_time(
        depth,
        5,
        feed,
    )

    cool = coolant(material)

    text = f"""
🕳 СВЕРЛЕНИЕ

Материал:
{material}

Сверло:
{tool}

Диаметр:
Ø{diameter:.1f}

Глубина:
{depth:.1f}

────────────────

Vc:
{vc} м/мин

S:
{rpm} об/мин

fn:
{fn:.2f} мм/об

F:
{feed} мм/мин

────────────────

Цикл:

{cycle}
"""

    if cycle == "G83":

        text += f"""

Шаг вывода:

{step} мм
"""

    text += f"""

────────────────

Охлаждение:

{cool}

────────────────

Время:

≈ {time_sec} сек
"""

    await message.answer(text)

    await state.clear()