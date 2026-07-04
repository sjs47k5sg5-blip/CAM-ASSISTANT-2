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
from keyboards.zero import zero_keyboard
from keyboards.finish import finish_keyboard
from keyboards.zero_z import zero_z_keyboard
from keyboards.finish_tool import finish_tool_keyboard
from keyboards.finish_modes import finish_modes_keyboard
from keyboards.corner_type import corner_type_keyboard
from keyboards.corner_select import corner_select_keyboard

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
        tool=message.text,
    )

    await state.set_state(
        ContourState.tool_number,
    )

    await message.answer(
        "Введите номер инструмента:"
    )


@router.message(ContourState.tool_number)
async def contour_tool_number(
    message: Message,
    state: FSMContext,
):

    try:
        tool = int(message.text)
    except ValueError:
        await message.answer(
            "Введите номер инструмента."
        )
        return

    await state.update_data(
        tool_number=tool,
    )

    await state.set_state(
        ContourState.diameter,
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

    await state.set_state(
        ContourState.corner_type,
    )

    await message.answer(
        "Обработать углы?",
        reply_markup=corner_type_keyboard,
    )


@router.message(ContourState.corner_type)
async def contour_corner_type(
    message: Message,
    state: FSMContext,
):

    if message.text == "⬜ Без обработки":

        await state.update_data(
            corner_type="none",
            corner_select="all",
            corner_value=0,
        )

        await state.set_state(
            ContourState.depth,
        )

        await message.answer(
            "Введите глубину обработки Z (мм):"
        )

        return

    elif message.text == "⭕ Радиусы":

        await state.update_data(
            corner_type="radius",
        )

    elif message.text == "🔷 Фаски":

        await state.update_data(
            corner_type="chamfer",
        )

    else:

        await message.answer(
            "Выберите вариант кнопкой.",
            reply_markup=corner_type_keyboard,
        )

        return

    await state.set_state(
        ContourState.corner_select,
    )

    await message.answer(
        "Какие углы обработать?",
        reply_markup=corner_select_keyboard,
    )


@router.message(ContourState.corner_select)
async def contour_corner_select(
    message: Message,
    state: FSMContext,
):

    await state.update_data(
        corner_select=message.text,
    )

    await state.set_state(
        ContourState.corner_value,
    )

    data = await state.get_data()

    if data["corner_type"] == "radius":
        text = "Введите радиус (мм):"
    else:
        text = "Введите размер фаски (мм):"

    await message.answer(text)


@router.message(ContourState.corner_value)
async def contour_corner_value(
    message: Message,
    state: FSMContext,
):

    try:
        value = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число.")
        return

    if value <= 0:
        await message.answer("Размер должен быть больше нуля.")
        return

    await state.update_data(
        corner_value=value,
    )

    await state.set_state(
        ContourState.depth,
    )

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

    await state.update_data(
        allowance=allowance,
    )

    if allowance == 0:

        await state.update_data(
            finish=False,
        )

        await state.set_state(
            ContourState.direction,
        )

        await message.answer(
            "Выберите направление фрезерования",
            reply_markup=direction_keyboard,
        )

        return

    await state.set_state(
        ContourState.finish,
    )

    await message.answer(
        "🧹 Выполнить чистовой проход?",
        reply_markup=finish_keyboard,
    )
    
@router.message(ContourState.finish)
async def contour_finish(message: Message, state: FSMContext):

    if message.text == "✅ Да":

        await state.update_data(
            finish=True,
        )

        await state.set_state(
            ContourState.finish_tool,
        )

        await message.answer(
            "Каким инструментом выполнить чистовой проход?",
            reply_markup=finish_tool_keyboard,
        )

        return

    elif message.text == "❌ Нет":

        await state.update_data(
            finish=False,
        )

        await state.set_state(
            ContourState.direction,
        )

        await message.answer(
            "Выберите направление фрезерования",
            reply_markup=direction_keyboard,
        )

        return

    await message.answer(
        "Выберите вариант кнопкой.",
        reply_markup=finish_keyboard,
    ) 


@router.message(ContourState.finish_tool)
async def contour_finish_tool(
    message: Message,
    state: FSMContext,
):

    if message.text == "✅ Тем же инструментом":

        await state.update_data(
            finish_same_tool=True,
        )

        await state.set_state(
            ContourState.finish_modes,
        )

        await message.answer(
            "Использовать режимы черновой обработки?",
            reply_markup=finish_modes_keyboard,
        )

        return

    if message.text == "🔄 Выбрать другой инструмент":

        await state.update_data(
            finish_same_tool=False,
        )

        await state.set_state(
            ContourState.finish_tool_number,
        )

        await message.answer(
            "Введите номер чистового инструмента:"
        )

        return

    await message.answer(
        "Выберите вариант кнопкой.",
        reply_markup=finish_tool_keyboard,
    )


@router.message(ContourState.finish_modes)
async def contour_finish_modes(
    message: Message,
    state: FSMContext,
):

    if message.text == "✅ Использовать те же режимы":

        await state.update_data(
            finish_same_modes=True,
        )

        await state.set_state(
            ContourState.direction,
        )

        await message.answer(
            "Выберите направление фрезерования",
            reply_markup=direction_keyboard,
        )

        return

    if message.text == "✏️ Изменить режимы":

        await state.update_data(
            finish_same_modes=False,
        )

        await state.set_state(
            ContourState.finish_rpm,
        )

        await message.answer(
            "Введите обороты чистовой обработки S:"
        )

        return

    await message.answer(
        "Выберите вариант кнопкой.",
        reply_markup=finish_modes_keyboard,
    )


@router.message(ContourState.finish_rpm)
async def contour_finish_rpm(
    message: Message,
    state: FSMContext,
):

    try:
        rpm = int(message.text)
    except ValueError:
        await message.answer("Введите целое число.")
        return

    await state.update_data(
        finish_rpm=rpm,
    )

    await state.set_state(
        ContourState.finish_feed,
    )

    await message.answer(
        "Введите подачу чистовой обработки F:"
    )


@router.message(ContourState.finish_feed)
async def contour_finish_feed(
    message: Message,
    state: FSMContext,
):

    try:
        feed = int(message.text)
    except ValueError:
        await message.answer("Введите целое число.")
        return

    await state.update_data(
        finish_feed=feed,
    )

    await state.set_state(
        ContourState.direction,
    )

    await message.answer(
        "Выберите направление фрезерования",
        reply_markup=direction_keyboard,
    )


@router.message(ContourState.finish_tool_number)
async def contour_finish_tool_number(
    message: Message,
    state: FSMContext,
):

    try:
        tool = int(message.text)
    except ValueError:
        await message.answer("Введите номер инструмента.")
        return

    await state.update_data(
        finish_tool_number=tool,
    )

    await state.set_state(
        ContourState.finish_tool_type,
    )

    await message.answer(
        "Выберите тип чистового инструмента:",
        reply_markup=milling_tools_keyboard,
    )


@router.message(ContourState.finish_tool_type)
async def contour_finish_tool_type(
    message: Message,
    state: FSMContext,
):

    await state.update_data(
        finish_tool=message.text,
    )

    await state.set_state(
        ContourState.finish_tool_diameter,
    )

    await message.answer(
        "Введите диаметр чистовой фрезы (мм):"
    )


@router.message(ContourState.finish_tool_diameter)
async def contour_finish_tool_diameter(
    message: Message,
    state: FSMContext,
):

    try:
        diameter = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число.")
        return

    await state.update_data(
        finish_diameter=diameter,
    )

    await state.set_state(
        ContourState.finish_tool_teeth,
    )

    await message.answer(
        "Введите количество зубьев:"
    )


@router.message(ContourState.finish_tool_teeth)
async def contour_finish_tool_teeth(
    message: Message,
    state: FSMContext,
):

    try:
        teeth = int(message.text)
    except ValueError:
        await message.answer("Введите целое число.")
        return

    await state.update_data(
        finish_teeth=teeth,
    )

    await state.set_state(
        ContourState.finish_rpm,
    )

    await message.answer(
        "Введите обороты чистовой обработки S:"
    )


@router.message(ContourState.direction)
async def contour_direction(message: Message, state: FSMContext):

    direction = message.text

    if direction not in ("➡️ Попутное", "⬅️ Встречное"):
        await message.answer(
            "Выберите направление кнопкой.",
            reply_markup=direction_keyboard,
        )
        return

    await state.update_data(direction=direction)

    await state.set_state(ContourState.zero)

    await message.answer(
        "🎯 Выберите ноль детали",
        reply_markup=zero_keyboard,
    )


@router.message(ContourState.zero)
async def contour_zero(message: Message, state: FSMContext):

    zero = message.text

    if zero not in (
        "↙️ Левый нижний",
        "↖️ Левый верхний",
        "↘️ Правый нижний",
        "↗️ Правый верхний",
        "⭕ Центр детали",
    ):
        await message.answer(
            "Выберите ноль детали кнопкой.",
            reply_markup=zero_keyboard,
        )
        return

    await state.update_data(zero=zero)

    await state.set_state(ContourState.zero_z)

    await message.answer(
    "Выберите ноль по Z:",
    reply_markup=zero_z_keyboard,
)


@router.message(ContourState.zero_z)
async def contour_zero_z(message: Message, state: FSMContext):

    if message.text not in (
        "⬆️ Верх детали",
        "⬇️ Низ детали",
    ):
        await message.answer(
            "Выберите вариант кнопкой.",
            reply_markup=zero_z_keyboard,
        )
        return

    await state.update_data(
        zero_z=message.text,
    )

    await state.set_state(
        ContourState.thickness,
    )

    await message.answer(
        "Введите толщину заготовки (мм):",
    )


@router.message(ContourState.thickness)
async def contour_thickness(message: Message, state: FSMContext):

    try:
        thickness = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число.")
        return

    await state.update_data(
        thickness=thickness
    )

    data = await state.get_data()

    direction = data["direction"]

    try:
        modes = get_modes(
            data["material"],
            data["tool"],
        )
        
        finish_modes = modes

        if not data.get("finish_same_tool", True):

            finish_modes = get_modes(
                data["material"],
                data["finish_tool"],
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
        tool=data["tool_number"],
        rpm=data["rpm"],
        feed=feed,
        length=data["length"],
        width=data["width"],
        depth=data["depth"],
        step=data["step"],
        allowance=data["allowance"],
        finish=data["finish"],
        outside=outside,
        climb=climb,
        zero=data["zero"],
        zero_z=data["zero_z"],
        thickness=data["thickness"],
        finish_same_tool=data.get("finish_same_tool", True),
        finish_tool=data.get("finish_tool_number", 1),
        finish_rpm=data.get("finish_rpm", data["rpm"]),
        finish_feed=data.get(
            "finish_feed",
            contour_feed(
                data["rpm"],
                data["finish_teeth"]
                if not data.get("finish_same_tool", True)
                else data["teeth"],
                finish_modes["fz"],
            ),
        ),
                 corner_type=data.get("corner_type", "none"),
        corner_select=data.get("corner_select", "all"),
        corner_value=data.get("corner_value", 0),
    )
    filename = "CONTOUR.nc"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(gcode)

    await message.answer(
        f"""
⭕ КОНТУР

Тип:
{data["side"]}

Ноль детали:
{data["zero"]}

Ноль по Z:
{data["zero_z"]}

Толщина заготовки:
{data["thickness"]} мм

Материал:
{data["material"]}

Инструмент:
{data["tool"]}

Диаметр:
Ø{data["diameter"]:.1f} мм

Подача:
F{feed}

Обороты:
S{data["rpm"]}

📄 G-код сохранён в файле CONTOUR.nc
""",
        reply_markup=main_menu,
    )

    await message.answer_document(
        FSInputFile(filename),
        caption="📄 CONTOUR.nc",
    )

    await state.clear()