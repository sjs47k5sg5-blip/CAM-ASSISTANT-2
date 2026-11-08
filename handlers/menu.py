from __future__ import annotations

import math

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile, KeyboardButton, Message, ReplyKeyboardMarkup

router = Router()


class Calculator(StatesGroup):
    drilling = State()
    drilling_points = State()
    thread = State()
    thread_points = State()
    cutting = State()


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📐 Контур")],
            [KeyboardButton(text="🕳 Сверление"), KeyboardButton(text="🧵 Резьба")],
            [KeyboardButton(text="⚙ Режимы резания")],
            [KeyboardButton(text="📚 Справочник"), KeyboardButton(text="ℹ О программе")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите операцию",
    )


def parse_points(raw: str, expected: int) -> list[tuple[float, float]]:
    points = []
    for line in raw.strip().splitlines():
        values = line.replace(",", ".").split()
        if len(values) != 2:
            raise ValueError("Каждая строка должна содержать X и Y.")
        x, y = map(float, values)
        if abs(x) > 1350 or abs(y) > 700:
            raise ValueError("Координата выходит за рабочий ход станка.")
        points.append((x, y))
    if len(points) != expected:
        raise ValueError(f"Ожидалось координат: {expected}, получено: {len(points)}.")
    return points


def make_header(tool: int, rpm: int, comment: str) -> list[str]:
    return [
        "%",
        f"O1002 ({comment})",
        "G21 G17 G90 G40 G49 G80",
        "G54",
        f"T{tool} M6",
        f"S{rpm} M3",
        f"G43 H{tool} Z100.000",
        "M8",
    ]


def make_footer() -> list[str]:
    return ["G80", "G00 Z100.000", "M9", "M5", "G49", "G91 G28 Z0.", "G90", "M30", "%"]


@router.message(F.text.in_({"/start", "/menu", "⬅ В меню"}))
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "🤖 <b>CAM Assistant</b>\n\nВыберите операцию. Любую УП проверьте в симуляторе перед запуском.",
        reply_markup=main_menu(),
    )


@router.message(F.text == "ℹ О программе")
async def about(message: Message) -> None:
    await message.answer(
        "<b>CAM Assistant</b>\nПомощник наладчика ЧПУ: контурная УП Fanuc, сверление, резьба и расчёт режимов."
    )


@router.message(F.text == "📚 Справочник")
async def handbook(message: Message) -> None:
    await message.answer(
        "<b>Краткий справочник</b>\nG00 — быстрый ход; G01 — линейная подача; G02/G03 — дуга; "
        "G17 — плоскость XY; G21 — миллиметры; G40 — отмена коррекции; G43 — коррекция длины; "
        "G54 — рабочая система; M03 — шпиндель; M08/M09 — СОЖ; M30 — конец программы."
    )


@router.message(F.text == "🕳 Сверление")
async def drilling_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Calculator.drilling)
    await message.answer(
        "Введите: <b>диаметр глубина число_отверстий обороты подача номер_инструмента</b>\n"
        "Пример: <code>8 20 4 1500 120 3</code>\nВсе размеры в мм, подача в мм/мин."
    )


@router.message(Calculator.drilling)
async def drilling_input(message: Message, state: FSMContext) -> None:
    try:
        d, depth, count, rpm, feed, tool = map(float, message.text.replace(",", ".").split())
        if min(d, depth, count, rpm, feed, tool) <= 0 or not count.is_integer() or not tool.is_integer():
            raise ValueError
        if count > 100 or tool > 30 or rpm > 15000 or feed > 15000:
            raise ValueError
    except (ValueError, AttributeError):
        await message.answer("Неверно. Пример: <code>8 20 4 1500 120 3</code>")
        return
    await state.update_data(drill_d=d, drill_depth=depth, drill_count=int(count),
                            drill_rpm=int(rpm), drill_feed=feed, drill_tool=int(tool))
    await state.set_state(Calculator.drilling_points)
    await message.answer(
        f"Теперь отправьте координаты X Y для {int(count)} отверстий, каждую пару с новой строки.\n"
        "Пример:\n<code>0 0\n20 0\n20 20\n0 20</code>"
    )


@router.message(Calculator.drilling_points)
async def drilling_points(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    try:
        points = parse_points(message.text, data["drill_count"])
    except (ValueError, AttributeError) as exc:
        await message.answer(f"Ошибка координат: {exc}")
        return
    d, depth = data["drill_d"], data["drill_depth"]
    lines = make_header(data["drill_tool"], data["drill_rpm"], "DRILLING - VERIFY")
    lines.append(f"G00 X{points[0][0]:.3f} Y{points[0][1]:.3f}")
    if depth > 3 * d:
        q = min(3.0, depth / 3)
        lines.append(f"G99 G83 Z-{depth:.3f} R2.000 Q{q:.3f} F{data['drill_feed']:.1f}")
    else:
        lines.append(f"G99 G81 Z-{depth:.3f} R2.000 F{data['drill_feed']:.1f}")
    for x, y in points[1:]:
        lines.append(f"G00 X{x:.3f} Y{y:.3f}")
    lines.extend(make_footer())
    await state.clear()
    await message.answer_document(
        BufferedInputFile(("\n".join(lines) + "\n").encode(), filename="drilling_fanuc.nc"),
        caption="УП сверления создана. Проверьте координаты, длину инструмента, R-плоскость и глубину.",
        reply_markup=main_menu(),
    )


@router.message(F.text == "🧵 Резьба")
async def thread_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Calculator.thread)
    await message.answer(
        "Введите: <b>диаметр шаг глубина обороты номер_инструмента</b>\n"
        "Пример: <code>10 1.5 15 500 4</code>"
    )


@router.message(Calculator.thread)
async def thread_input(message: Message, state: FSMContext) -> None:
    try:
        diameter, pitch, depth, rpm, tool = map(float, message.text.replace(",", ".").split())
        if min(diameter, pitch, depth, rpm, tool) <= 0 or not tool.is_integer():
            raise ValueError
        if rpm > 15000 or tool > 30:
            raise ValueError
    except (ValueError, AttributeError):
        await message.answer("Неверно. Пример: <code>10 1.5 15 500 4</code>")
        return
    await state.update_data(thread_d=diameter, thread_pitch=pitch, thread_depth=depth,
                            thread_rpm=int(rpm), thread_tool=int(tool))
    await state.set_state(Calculator.thread_points)
    await message.answer("Отправьте координаты отверстий X Y, по одной паре на строку.")


@router.message(Calculator.thread_points)
async def thread_points(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    raw_lines = message.text.strip().splitlines()
    try:
        points = parse_points(message.text, len(raw_lines))
        if not points:
            raise ValueError("Нужна хотя бы одна координата.")
    except (ValueError, AttributeError) as exc:
        await message.answer(f"Ошибка координат: {exc}")
        return
    feed = data["thread_rpm"] * data["thread_pitch"]
    lines = make_header(data["thread_tool"], data["thread_rpm"], "TAPPING - VERIFY")
    lines.append(f"G00 X{points[0][0]:.3f} Y{points[0][1]:.3f}")
    lines.append(f"G99 G84 Z-{data['thread_depth']:.3f} R2.000 F{feed:.3f}")
    for x, y in points[1:]:
        lines.append(f"G00 X{x:.3f} Y{y:.3f}")
    lines.extend(make_footer())
    await state.clear()
    await message.answer_document(
        BufferedInputFile(("\n".join(lines) + "\n").encode(), filename="tapping_fanuc.nc"),
        caption=f"УП резьбонарезания создана. Расчётная подача F=S×P={feed:.3f} мм/мин. Проверьте метчик и G84.",
        reply_markup=main_menu(),
    )


@router.message(F.text == "⚙ Режимы резания")
async def cutting_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Calculator.cutting)
    await message.answer(
        "Введите: <b>диаметр число_зубьев Vc fz</b>\nПример: <code>10 4 120 0.03</code>\n"
        "Vc — м/мин, fz — мм/зуб."
    )


@router.message(Calculator.cutting)
async def cutting_input(message: Message, state: FSMContext) -> None:
    try:
        diameter, teeth, vc, fz = map(float, message.text.replace(",", ".").split())
        if min(diameter, teeth, vc, fz) <= 0:
            raise ValueError
    except (ValueError, AttributeError):
        await message.answer("Пример ввода: <code>10 4 120 0.03</code>")
        return
    rpm = min(15000, (1000 * vc) / (math.pi * diameter))
    feed = rpm * teeth * fz
    await state.clear()
    await message.answer(
        f"<b>Расчёт режимов</b>\nS ≈ <b>{rpm:.0f} об/мин</b>\nF ≈ <b>{feed:.0f} мм/мин</b>\n"
        "Проверьте режим по материалу, типу фрезы, вылету и рекомендациям производителя.",
        reply_markup=main_menu(),
    )


@router.message(F.text)
async def unknown(message: Message) -> None:
    await message.answer("Не понял команду. Нажмите /start и выберите раздел.")
