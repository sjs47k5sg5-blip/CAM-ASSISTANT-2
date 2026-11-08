from __future__ import annotations

import math

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    BufferedInputFile,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

router = Router()


class ContourWizard(StatesGroup):
    size = State()
    tool = State()
    corner = State()
    step = State()
    feeds = State()


def kb(rows: list[list[tuple[str, str]]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=label, callback_data=data) for label, data in row]
        for row in rows
    ])


async def show_menu(target: Message | CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    checks = [
        ("Размер", all(data.get(k) for k in ("x", "y", "z"))),
        ("Ноль XY", bool(data.get("zero"))),
        ("Ноль Z", bool(data.get("zero_z"))),
        ("Инструмент", bool(data.get("tool_d"))),
        ("Углы", data.get("corner") is not None),
        ("Режимы", bool(data.get("rpm") and data.get("feed") and data.get("step_z"))),
    ]
    text = "<b>📐 Мастер контура</b>\n\n" + "\n".join(
        f"{'✅' if ok else '▫️'} {name}" for name, ok in checks
    ) + "\n\nВыберите параметр:"
    keyboard = kb([
        [("📏 Размер X Y Z", "cam:size")],
        [("📍 Ноль XY", "cam:zero")],
        [("📍 Ноль Z", "cam:zeroz")],
        [("🔧 Инструмент T и Ø", "cam:tool")],
        [("Углы: острые / радиус", "cam:corner")],
        [("📉 Шаг по Z и припуск", "cam:step")],
        [("⚙ Обороты и подача", "cam:feeds")],
        [("▶ Проверить и создать УП", "cam:generate")],
        [("⬅ В меню", "cam:exit")],
    ])
    if isinstance(target, CallbackQuery):
        try:
            await target.message.edit_text(text, reply_markup=keyboard)
        except TelegramBadRequest:
            await target.message.answer(text, reply_markup=keyboard)
        await target.answer()
    else:
        await target.answer(text, reply_markup=keyboard)


@router.message(F.text == "📐 Контур")
async def start_contour(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.update_data(
        zero="CENTER", zero_z="TOP", corner="SHARP", corner_r=0.0,
        step_z=2.0, allowance=0.0, rpm=1500, feed=150,
        safe_z=100.0, approach_z=5.0,
    )
    await show_menu(message, state)


@router.callback_query(F.data.startswith("cam:"))
async def contour_actions(callback: CallbackQuery, state: FSMContext) -> None:
    action = callback.data.split(":", 1)[1]
    if action == "exit":
        await state.clear()
        await callback.message.answer("Возврат в главное меню. Нажмите /start.")
        await callback.answer()
        return
    if action == "zero":
        await callback.message.edit_text(
            "Выберите ноль XY:",
            reply_markup=kb([
                [("Центр", "camset:zero:CENTER")],
                [("Левый нижний", "camset:zero:BL"), ("Правый нижний", "camset:zero:BR")],
                [("Левый верхний", "camset:zero:TL"), ("Правый верхний", "camset:zero:TR")],
                [("⬅ Назад", "cam:menu")],
            ]),
        )
    elif action == "zeroz":
        await callback.message.edit_text(
            "Выберите ноль Z:",
            reply_markup=kb([
                [("Верх детали", "camset:zero_z:TOP")],
                [("Низ детали", "camset:zero_z:BOTTOM")],
                [("⬅ Назад", "cam:menu")],
            ]),
        )
    elif action == "menu":
        await show_menu(callback, state)
        return
    elif action in {"size", "tool", "corner", "step", "feeds"}:
        prompts = {
            "size": ("Введите габариты заготовки X Y Z в мм. Пример: <code>30 20 15</code>", ContourWizard.size),
            "tool": ("Введите номер инструмента и диаметр фрезы. Пример: <code>3 10</code>", ContourWizard.tool),
            "corner": ("Выберите тип углов:", ContourWizard.corner),
            "step": ("Введите шаг по Z и боковой припуск на сторону в мм. Пример: <code>2 0.2</code>", ContourWizard.step),
            "feeds": ("Введите обороты и подачу в мм/мин. Пример: <code>1500 150</code>", ContourWizard.feeds),
        }
        prompt, fsm_state = prompts[action]
        if action == "corner":
            await callback.message.edit_text(prompt, reply_markup=kb([
                [("Острые углы", "camset:corner:SHARP")],
                [("Радиус (ввести значение)", "camset:corner:RADIUS")],
                [("⬅ Назад", "cam:menu")],
            ]))
        else:
            await state.set_state(fsm_state)
            await callback.message.answer(prompt)
    elif action == "generate":
        await generate(callback, state)
        return
    await callback.answer()


@router.callback_query(F.data.startswith("camset:"))
async def contour_set(callback: CallbackQuery, state: FSMContext) -> None:
    _, field, value = callback.data.split(":", 2)
    if field == "corner" and value == "RADIUS":
        await state.set_state(ContourWizard.corner)
        await callback.message.answer("Введите радиус угла в мм, например <code>2</code>.")
    else:
        await state.update_data(**{field: value})
        await show_menu(callback, state)


@router.message(ContourWizard.size)
async def input_size(message: Message, state: FSMContext) -> None:
    try:
        x, y, z = map(float, message.text.replace(",", ".").split())
        if min(x, y, z) <= 0 or max(x, y, z) > 1350:
            raise ValueError
    except (ValueError, AttributeError):
        await message.answer("Нужны три положительных размера в мм. Пример: <code>30 20 15</code>")
        return
    await state.update_data(x=x, y=y, z=z)
    await state.set_state(None)
    await show_menu(message, state)


@router.message(ContourWizard.tool)
async def input_tool(message: Message, state: FSMContext) -> None:
    try:
        number_s, diameter_s = message.text.replace(",", ".").split()
        number, diameter = int(number_s), float(diameter_s)
        if not 1 <= number <= 30 or diameter <= 0 or diameter > 100:
            raise ValueError
    except (ValueError, AttributeError):
        await message.answer("Формат: <code>номер Ø</code>, например <code>3 10</code>.")
        return
    await state.update_data(tool=number, tool_d=diameter)
    await state.set_state(None)
    await show_menu(message, state)


@router.message(ContourWizard.corner)
async def input_corner_radius(message: Message, state: FSMContext) -> None:
    try:
        radius = float(message.text.replace(",", "."))
        data = await state.get_data()
        if radius <= 0 or radius > min(data.get("x", 0), data.get("y", 0)) / 2:
            raise ValueError
    except (ValueError, AttributeError):
        await message.answer("Введите положительный радиус, не превышающий половины меньшего размера.")
        return
    await state.update_data(corner="RADIUS", corner_r=radius)
    await state.set_state(None)
    await show_menu(message, state)


@router.message(ContourWizard.step)
async def input_step(message: Message, state: FSMContext) -> None:
    try:
        step_z, allowance = map(float, message.text.replace(",", ".").split())
        if step_z <= 0 or step_z > 10 or allowance < 0 or allowance > 5:
            raise ValueError
    except (ValueError, AttributeError):
        await message.answer("Введите два числа: шаг Z (0–10) и припуск (0–5). Пример: <code>2 0.2</code>")
        return
    await state.update_data(step_z=step_z, allowance=allowance)
    await state.set_state(None)
    await show_menu(message, state)


@router.message(ContourWizard.feeds)
async def input_feeds(message: Message, state: FSMContext) -> None:
    try:
        rpm_s, feed_s = message.text.replace(",", ".").split()
        rpm, feed = int(rpm_s), float(feed_s)
        if not 100 <= rpm <= 15000 or not 1 <= feed <= 15000:
            raise ValueError
    except (ValueError, AttributeError):
        await message.answer("Обороты 100–15000, подача 1–15000. Пример: <code>1500 150</code>")
        return
    await state.update_data(rpm=rpm, feed=feed)
    await state.set_state(None)
    await show_menu(message, state)


def z_passes(thickness: float, step: float, zero_z: str) -> list[float]:
    count = math.ceil(thickness / step)
    depths = [min(i * step, thickness) for i in range(1, count + 1)]
    if zero_z == "TOP":
        return [-round(d, 4) for d in depths]
    return [round(thickness - d, 4) for d in depths]


def rounded_rectangle_gcode(x: float, y: float, tool_r: float, corner_r: float,
                            zero: str, z: float, feed: float) -> list[str]:
    if zero == "CENTER":
        x0, y0 = -x / 2, -y / 2
    elif zero == "TL":
        x0, y0 = 0.0, -y
    elif zero == "TR":
        x0, y0 = -x, -y
    elif zero == "BR":
        x0, y0 = -x, 0.0
    else:
        x0, y0 = 0.0, 0.0
    x0 -= tool_r
    y0 -= tool_r
    x1, y1 = x0 + x + 2 * tool_r, y0 + y + 2 * tool_r
    r = tool_r + corner_r
    if r <= 0 or r >= min(x1 - x0, y1 - y0) / 2:
        raise ValueError("Радиус траектории недопустим для выбранных размеров и фрезы.")
    points = [
        (x0 + r, y0), (x1 - r, y0),
        (x1, y0 + r), (x1, y1 - r),
        (x1 - r, y1), (x0 + r, y1),
        (x0, y1 - r), (x0, y0 + r),
        (x0 + r, y0),
    ]
    lines = [f"G00 X{points[0][0]:.3f} Y{points[0][1]:.3f}", f"G01 Z{z:.3f} F{feed:.1f}"]
    centers = [
        (x1 - r, y0 + r), (x1 - r, y1 - r),
        (x0 + r, y1 - r), (x0 + r, y0 + r),
    ]
    for i in range(4):
        end = points[2 * i + 2]
        start = points[2 * i + 1]
        lines.append(f"G01 X{start[0]:.3f} Y{start[1]:.3f} F{feed:.1f}")
        cx, cy = centers[i]
        lines.append(
            f"G03 X{end[0]:.3f} Y{end[1]:.3f} I{cx-start[0]:.3f} J{cy-start[1]:.3f} F{feed:.1f}"
        )
        if i < 3:
            nxt = points[2 * i + 3]
            lines.append(f"G01 X{nxt[0]:.3f} Y{nxt[1]:.3f} F{feed:.1f}")
    return lines


async def generate(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    required = ("x", "y", "z", "tool", "tool_d", "zero", "zero_z", "rpm", "feed", "step_z")
    missing = [key for key in required if data.get(key) is None]
    if missing:
        await callback.answer("Заполните все параметры.", show_alert=True)
        return
    if data["tool_d"] >= min(data["x"], data["y"]):
        await callback.answer("Диаметр фрезы слишком велик для детали.", show_alert=True)
        return
    try:
        levels = z_passes(data["z"], data["step_z"], data["zero_z"])
        lines = [
            "%",
            "O1001 (CAM ASSISTANT - VERIFY BEFORE USE)",
            "G21 G17 G90 G40 G49 G80",
            "G54",
            f"T{data['tool']} M6",
            f"S{data['rpm']} M3",
            f"G43 H{data['tool']} Z100.000",
            "M8",
        ]
        for z in levels:
            lines.append("G00 Z5.000")
            lines.extend(rounded_rectangle_gcode(
                data["x"], data["y"], data["tool_d"] / 2,
                data.get("corner_r", 0.0) if data.get("corner") == "RADIUS" else 0.0,
                data["zero"], z, data["feed"],
            ))
        lines.extend(["G00 Z100.000", "M9", "M5", "G49", "G91 G28 Z0.", "G90", "M30", "%"])
        program = "\n".join(lines) + "\n"
    except ValueError as exc:
        await callback.message.answer(f"Не удалось построить траекторию: {exc}")
        await callback.answer()
        return
    filename = "contour_fanuc.nc"
    await callback.message.answer_document(
        BufferedInputFile(program.encode("utf-8"), filename=filename),
        caption=(
            "Файл создан. Это черновая УП: проверьте систему координат, Z0, вылет инструмента, "
            "коррекцию длины, безопасные высоты и траекторию в симуляторе. Не запускайте без проверки."
        ),
    )
    await callback.answer("G-код сформирован.")
