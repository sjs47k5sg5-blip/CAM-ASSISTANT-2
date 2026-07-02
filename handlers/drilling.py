from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import DrillingState
from keyboards.materials import materials_keyboard
from keyboards.drilling import drill_type_keyboard

from services.drilling import (
    spindle_speed,
    feed_rate,
    get_cutting_data,
    drilling_cycle,
    drilling_time,
    coolant,
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
    if message.text not in ("HSS", "Твердосплавное"):
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
        vc, fn = get_cutting_data(material, tool, diameter)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")
        await state.clear()
        return

    rpm = spindle_speed(vc, diameter)
    feed = feed_rate(rpm, fn)

    cycle, step = drilling_cycle(depth, diameter)

    time_sec = drilling_time(depth, 5, feed)

    cool = coolant(material)

    text = (
        f"🕳 СВЕРЛЕНИЕ\n\n"
        f"Материал: {material}\n"
        f"Тип сверла: {tool}\n"
        f"Диаметр: Ø{diameter:.1f} мм\n"
        f"Глубина: {depth:.1f} мм\n\n"
        f"Vc: {vc} м/мин\n"
        f"S: {rpm} об/мин\n"
        f"fn: {fn:.2f} мм/об\n"
        f"F: {feed} мм/мин\n\n"
        f"Цикл: {cycle}\n"
    )

    if cycle == "G83":
        text += f"\nШаг вывода сверла: {step} мм\n"

    text += (
        f"\nОхлаждение: {cool}\n"
        f"\nВремя: ≈ {time_sec} сек"
    )

    await message.answer(text)

    await state.clear()