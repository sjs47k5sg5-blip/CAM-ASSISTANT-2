from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import ToleranceState

from keyboards.main_menu import main_menu
from keyboards.reference import reference_keyboard
from keyboards.thread_reference import thread_reference_keyboard
from keyboards.gcodes import gcodes_keyboard
from keyboards.mcodes import mcodes_keyboard
from keyboards.tolerances import tolerances_keyboard

from services.iso286 import (
    calculate_hole_h,
    calculate_shaft_h,
)

router = Router()


# ==========================
# СПРАВОЧНИК
# ==========================

@router.message(F.text == "📚 Справочник")
async def reference_menu(message: Message):

    await message.answer(
        "📚 Справочник",
        reply_markup=reference_keyboard,
    )


# ==========================
# РЕЗЬБЫ
# ==========================

THREADS = {

    "M3":
"""🔩 M3

Диаметр:
3 мм

Шаг:
0.5 мм

Сверло:
2.5 мм
""",

    "M4":
"""🔩 M4

Диаметр:
4 мм

Шаг:
0.7 мм

Сверло:
3.3 мм
""",

    "M5":
"""🔩 M5

Диаметр:
5 мм

Шаг:
0.8 мм

Сверло:
4.2 мм
""",

    "M6":
"""🔩 M6

Диаметр:
6 мм

Шаг:
1.0 мм

Сверло:
5.0 мм
""",

    "M8":
"""🔩 M8

Диаметр:
8 мм

Шаг:
1.25 мм

Сверло:
6.8 мм
""",

    "M10":
"""🔩 M10

Диаметр:
10 мм

Шаг:
1.5 мм

Сверло:
8.5 мм
""",

    "M12":
"""🔩 M12

Диаметр:
12 мм

Шаг:
1.75 мм

Сверло:
10.2 мм
""",
}


@router.message(F.text == "🔩 Резьбы")
async def thread_reference(message: Message):

    await message.answer(
        "Выберите резьбу",
        reply_markup=thread_reference_keyboard,
    )


@router.message(F.text.in_(THREADS.keys()))
async def thread_info(message: Message):

    await message.answer(
        THREADS[message.text]
    )
    
# ==========================
# G-КОДЫ
# ==========================

@router.message(F.text == "📘 G-коды")
async def gcodes_menu(message: Message):
    await message.answer(
        "Выберите G-код",
        reply_markup=gcodes_keyboard,
    )


G_CODES = {

    "G00": "G00 -- Быстрое перемещение",

    "G01": "G01 -- Линейная интерполяция",

    "G02": "G02 -- Круговая интерполяция по часовой стрелке",

    "G03": "G03 -- Круговая интерполяция против часовой стрелки",

    "G04": "G04 -- Выдержка",

    "G17": "G17 -- Плоскость XY",

    "G18": "G18 -- Плоскость ZX",

    "G19": "G19 -- Плоскость YZ",

    "G20": "G20 -- Дюймы",

    "G21": "G21 -- Миллиметры",

    "G28": "G28 -- Возврат в ноль станка",

    "G40": "G40 -- Отмена коррекции инструмента",

    "G41": "G41 -- Коррекция слева",

    "G42": "G42 -- Коррекция справа",

    "G43": "G43 -- Коррекция длины инструмента",

    "G49": "G49 -- Отмена коррекции длины",

    "G54": "G54 -- Смещение детали",

    "G80": "G80 -- Отмена цикла",

    "G81": "G81 -- Цикл сверления",

    "G83": "G83 -- Глубокое сверление",

    "G84": "G84 -- Нарезание резьбы",

    "G90": "G90 -- Абсолютные координаты",

    "G91": "G91 -- Относительные координаты",
}


@router.message(F.text.in_(G_CODES.keys()))
async def gcode_info(message: Message):
    await message.answer(G_CODES[message.text])


# ==========================
# M-КОДЫ
# ==========================

@router.message(F.text == "📙 M-коды")
async def mcodes_menu(message: Message):
    await message.answer(
        "Выберите M-код",
        reply_markup=mcodes_keyboard,
    )


M_CODES = {

    "M00": "M00 -- Останов программы",

    "M01": "M01 -- Опциональный останов",

    "M03": "M03 -- Шпиндель по часовой",

    "M04": "M04 -- Шпиндель против часовой",

    "M05": "M05 -- Останов шпинделя",

    "M06": "M06 -- Смена инструмента",

    "M08": "M08 -- СОЖ включить",

    "M09": "M09 -- СОЖ выключить",

    "M19": "M19 -- Ориентация шпинделя",

    "M29": "M29 -- Подготовка жесткого нарезания резьбы",

    "M30": "M30 -- Конец программы",

    "M98": "M98 -- Вызов подпрограммы",

    "M99": "M99 -- Возврат из подпрограммы"
}


@router.message(F.text.in_(M_CODES.keys()))
async def mcode_info(message: Message):
    await message.answer(M_CODES[message.text])
    
    # ==========================
# ДОПУСКИ ISO 286
# ==========================

FIELDS = [
    "H6", "H7", "H8", "H9", "H10", "H11", "H12",
    "h5", "h6", "h7", "h8", "h9", "h10", "h11"
]


@router.message(F.text == "📏 Допуски")
async def tolerance_menu(message: Message):

    await message.answer(
        "Выберите поле допуска",
        reply_markup=tolerances_keyboard,
    )


@router.message(F.text.in_(FIELDS))
async def tolerance_select(message: Message, state: FSMContext):

    await state.update_data(
        field=message.text
    )

    await state.set_state(
        ToleranceState.diameter
    )

    await message.answer(
        "Введите номинальный диаметр (мм):"
    )


@router.message(ToleranceState.diameter)
async def tolerance_result(message: Message, state: FSMContext):

    try:
        diameter = float(
            message.text.replace(",", ".")
        )
    except ValueError:
        await message.answer(
            "Введите число."
        )
        return

    data = await state.get_data()

    field = data["field"]

    grade = "IT" + "".join(filter(str.isdigit, field))

    if field.startswith("H"):

        result = calculate_hole_h(
            diameter,
            grade,
        )

        if result is None:
            await message.answer(
                "Диаметр вне диапазона."
            )
            await state.clear()
            return

        await message.answer(
f"""📏 Ø{diameter:g} {field}

EI = {result["ei"]:.3f}

ES = +{result["es"]:.3f}

Минимальный размер

{result["min"]:.3f}

Максимальный размер

{result["max"]:.3f}

Допуск

{result["tol"]:.3f} мм"""
        )

    else:

        result = calculate_shaft_h(
            diameter,
            grade,
        )

        if result is None:
            await message.answer(
                "Диаметр вне диапазона."
            )
            await state.clear()
            return

        await message.answer(
f"""📏 Ø{diameter:g} {field}

ei = {result["ei"]:.3f}

es = {result["es"]:.3f}

Минимальный размер

{result["min"]:.3f}

Максимальный размер

{result["max"]:.3f}

Допуск

{result["tol"]:.3f} мм"""
        )

    await state.clear()