from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.main_menu import main_menu
from keyboards.reference import reference_keyboard
from keyboards.thread_reference import thread_reference_keyboard
from keyboards.gcodes import gcodes_keyboard
from keyboards.mcodes import mcodes_keyboard
from keyboards.tolerances import tolerances_keyboard

from services.tolerance_service import get_tolerance

from states import ToleranceState

router = Router()


@router.message(F.text == "📚 Справочник")
async def reference_menu(message: Message):
    await message.answer(
        "📚 Выберите раздел справочника",
        reply_markup=reference_keyboard,
    )


@router.message(F.text == "🔩 Резьбы")
async def threads_menu(message: Message):
    await message.answer(
        "Выберите размер резьбы",
        reply_markup=thread_reference_keyboard,
    )


THREADS = {
    "M3": "🔩 M3\n\nШаг: 0.5 мм\nСверло: Ø2.5 мм",
    "M4": "🔩 M4\n\nШаг: 0.7 мм\nСверло: Ø3.3 мм",
    "M5": "🔩 M5\n\nШаг: 0.8 мм\nСверло: Ø4.2 мм",
    "M6": "🔩 M6\n\nШаг: 1.0 мм\nСверло: Ø5.0 мм",
    "M8": "🔩 M8\n\nШаг: 1.25 мм\nСверло: Ø6.8 мм",
    "M10": "🔩 M10\n\nШаг: 1.5 мм\nСверло: Ø8.5 мм",
    "M12": "🔩 M12\n\nШаг: 1.75 мм\nСверло: Ø10.2 мм",
    "M16": "🔩 M16\n\nШаг: 2.0 мм\nСверло: Ø14.0 мм",
    "M20": "🔩 M20\n\nШаг: 2.5 мм\nСверло: Ø17.5 мм",
}


@router.message(F.text.in_(THREADS.keys()))
async def thread_info(message: Message):
    await message.answer(THREADS[message.text])


@router.message(F.text == "⚙️ G-коды")
async def gcodes_menu(message: Message):
    await message.answer(
        "⚙️ Выберите G-код",
        reply_markup=gcodes_keyboard,
    )


G_CODES = {
    "G00": "⚙️ G00\n\nБыстрое перемещение.\n\nФормат:\nG00 X Y Z",
    "G01": "⚙️ G01\n\nЛинейная интерполяция.\n\nФормат:\nG01 X Y Z F",
    "G02": "⚙️ G02\n\nКруговая интерполяция по часовой стрелке.\n\nФормат:\nG02 X Y I J",
    "G03": "⚙️ G03\n\nКруговая интерполяция против часовой стрелки.\n\nФормат:\nG03 X Y I J",
    "G17": "⚙️ G17\n\nВыбор плоскости XY.",
    "G18": "⚙️ G18\n\nВыбор плоскости ZX.",
    "G19": "⚙️ G19\n\nВыбор плоскости YZ.",
    "G40": "⚙️ G40\n\nОтмена коррекции радиуса инструмента.",
    "G41": "⚙️ G41\n\nКоррекция радиуса слева.",
    "G42": "⚙️ G42\n\nКоррекция радиуса справа.",
    "G43": "⚙️ G43\n\nКоррекция длины инструмента.",
    "G54": "⚙️ G54\n\nРабочая система координат №1.",
    "G81": "⚙️ G81\n\nПростой цикл сверления.\n\nG81 X Y Z R F",
    "G83": "⚙️ G83\n\nЦикл глубокого сверления.\n\nG83 X Y Z Q R F",
    "G84": "⚙️ G84\n\nЦикл нарезания резьбы.\n\nG84 X Y Z R F",
}


@router.message(F.text.in_(G_CODES.keys()))
async def gcode_info(message: Message):
    await message.answer(G_CODES[message.text])


@router.message(F.text == "🔧 M-коды")
async def mcodes_menu(message: Message):
    await message.answer(
        "🔧 Выберите M-код",
        reply_markup=mcodes_keyboard,
    )


M_CODES = {

    "M00": """🔧 M00

Безусловный останов программы.

После нажатия Cycle Start программа продолжится.
""",

    "M01": """🔧 M01

Дополнительный останов программы.

Работает при включенном Optional Stop.
""",

    "M03": """🔧 M03

Вращение шпинделя по часовой стрелке.

Пример:

S1500 M03
""",

    "M04": """🔧 M04

Вращение шпинделя против часовой стрелки.

Пример:

S800 M04
""",

    "M05": """🔧 M05

Останов шпинделя.
""",

    "M06": """🔧 M06

Смена инструмента.

Пример:

T5 M06
""",

    "M08": """🔧 M08

Включить СОЖ.
""",

    "M09": """🔧 M09

Выключить СОЖ.
""",

    "M19": """🔧 M19

Ориентация шпинделя.
""",

    "M30": """🔧 M30

Конец программы.

Возврат в начало программы.
""",
}


@router.message(F.text.in_(M_CODES.keys()))
async def mcode_info(message: Message):
    await message.answer(
        M_CODES[message.text]
    )


@router.message(F.text == "📏 Допуски")
async def tolerances_menu(message: Message):
    await message.answer(
        "📏 Выберите поле допуска",
        reply_markup=tolerances_keyboard,
    )


TOLERANCES = {

    "H6": """📏 H6

Высокоточное отверстие.

Квалитет:
IT6

Применение:
Прецизионные соединения.
""",

    "H7": """📏 H7

Самое распространённое поле допуска отверстия.

Квалитет:
IT7

Используется с:
h6
g6
f7
""",

    "H8": """📏 H8

Средняя точность.

Квалитет:
IT8
""",

    "H9": """📏 H9

Нормальная точность.

Квалитет:
IT9
""",

    "H10": """📏 H10

Грубая обработка.

Квалитет:
IT10
""",

    "H11": """📏 H11

Очень распространённый допуск.

Применяется после сверления.

Квалитет:
IT11
""",

    "H12": """📏 H12

Черновая обработка.

Квалитет:
IT12
""",
}


@router.message(F.text.in_(TOLERANCES.keys()))
async def tolerance_info(message: Message):
    await message.answer(
        TOLERANCES[message.text]
    )


@router.message(ToleranceState.diameter)
async def tolerance_result(message: Message, state: FSMContext):

    try:
        diameter = float(message.text.replace(",", "."))

    except ValueError:
        await message.answer("❌ Введите число.")
        return

    data = await state.get_data()

    result = get_tolerance(
        data["tolerance"],
        diameter,
    )

    if result is None:
        await message.answer(
            "❌ Диаметр вне диапазона таблицы."
        )
        await state.clear()
        return

    await message.answer(
f"""📏 Ø{diameter:g} {data['tolerance']}

Минимальный размер:
{result['min']:.3f} мм

Максимальный размер:
{result['max']:.3f} мм

Допуск:
{result['tol']:.3f} мм""",
        reply_markup=reference_keyboard,
    )

    await state.clear()


@router.message(F.text == "⬅️ Назад")
async def reference_back(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "🏠 Главное меню",
        reply_markup=main_menu,
    )

