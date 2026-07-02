from keyboards.milling import milling_keyboard
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import MillingState

from keyboards.materials import materials_keyboard
from keyboards.tools import tools_keyboard
from keyboards.main_menu import main_menu

from services.material_service import get_modes
from services.cutting import spindle_speed, feed_rate

router = Router()
@router.message(F.text == "📐 Фрезерование")
async def milling_menu(message: Message, state: FSMContext):

    await state.clear()

    await message.answer(
        "📐 Выберите раздел фрезерования",
        reply_markup=milling_keyboard,
    )


@router.message(F.text == "📐 Режимы резания")
async def milling_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(MillingState.material)

    await message.answer(
        "📐 Выберите материал",
        reply_markup=materials_keyboard
    )


@router.message(MillingState.material)
async def material_selected(message: Message, state: FSMContext):

    material = message.text

    await state.update_data(material=material)

    await state.set_state(MillingState.tool)

    await message.answer(
        "🛠 Выберите инструмент",
        reply_markup=tools_keyboard
    )


@router.message(MillingState.tool)
async def tool_selected(message: Message, state: FSMContext):

    tool = message.text

    await state.update_data(tool=tool)

    await state.set_state(MillingState.diameter)

    await message.answer(
        "Введите диаметр фрезы (мм):"
    )


@router.message(MillingState.diameter)
async def diameter_selected(message: Message, state: FSMContext):

    try:
        diameter = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число.")
        return

    await state.update_data(diameter=diameter)

    await state.set_state(MillingState.teeth)

    await message.answer(
        "Введите количество зубьев:"
    )


@router.message(MillingState.teeth)
async def teeth_selected(message: Message, state: FSMContext):

    try:
        teeth = int(message.text)
    except ValueError:
        await message.answer("Введите целое число.")
        return

    data = await state.get_data()

    material = data["material"]
    tool = data["tool"]
    diameter = data["diameter"]

    try:
        modes = get_modes(material, tool)
    except KeyError:
        await message.answer(
            "❌ Для выбранного материала или инструмента нет режимов.",
            reply_markup=main_menu
        )
        await state.clear()
        return

    vc = modes["vc"]
    fz = modes["fz"]

    ap = diameter * modes["ap"]
    ae = diameter * modes["ae"]

    rpm = spindle_speed(vc, diameter)
    feed = feed_rate(rpm, teeth, fz)

    await message.answer(
        f"""
📐 РЕЖИМЫ РЕЗАНИЯ

Материал:
{material}

Инструмент:
{tool}

Диаметр:
Ø{diameter:.1f} мм

Количество зубьев:
{teeth}

────────────────

Vc:
{vc} м/мин

Fz:
{fz:.3f} мм/зуб

────────────────

Обороты шпинделя

S{rpm} об/мин

Подача

F{feed} мм/мин

────────────────

Ap

{ap:.1f} мм

Ae

{ae:.1f} мм
""",
        reply_markup=main_menu
    )

    await state.clear()