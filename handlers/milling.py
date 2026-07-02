from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import MillingState
from services.cutting import spindle_speed, feed_rate

router = Router()


@router.message(F.text == "📐 Режимы резания")
async def milling_start(message: Message, state: FSMContext):
    await state.set_state(MillingState.diameter)
    await message.answer("Введите диаметр фрезы (мм):")


@router.message(MillingState.diameter)
async def milling_diameter(message: Message, state: FSMContext):
    try:
        diameter = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число, например: 10")
        return

    await state.update_data(diameter=diameter)
    await state.set_state(MillingState.teeth)
    await message.answer("Введите количество зубьев:")


@router.message(MillingState.teeth)
async def milling_teeth(message: Message, state: FSMContext):
    try:
        teeth = int(message.text)
    except ValueError:
        await message.answer("Введите целое число.")
        return

    await state.update_data(teeth=teeth)
    await state.set_state(MillingState.vc)
    await message.answer("Введите скорость резания Vc (м/мин):")


@router.message(MillingState.vc)
async def milling_vc(message: Message, state: FSMContext):
    try:
        vc = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число.")
        return

    await state.update_data(vc=vc)
    await state.set_state(MillingState.fz)
    await message.answer("Введите подачу на зуб Fz (мм):")


@router.message(MillingState.fz)
async def milling_result(message: Message, state: FSMContext):
    try:
        fz = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число.")
        return

    data = await state.get_data()

    diameter = data["diameter"]
    teeth = data["teeth"]
    vc = data["vc"]

    rpm = spindle_speed(vc, diameter)
    feed = feed_rate(rpm, teeth, fz)

    await message.answer(
        f"""📐 Результат расчёта

Диаметр: Ø{diameter:g} мм
Количество зубьев: {teeth}

Vc = {vc} м/мин
Fz = {fz} мм

Обороты S = {rpm} об/мин
Подача F = {feed} мм/мин"""
    )

    await state.clear()