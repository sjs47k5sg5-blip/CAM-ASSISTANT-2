from __future__ import annotations

from services.cam_engine.simple_contour import build_contour_program

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
        if field == "corner" and value == "SHARP":
            await state.update_data(corner_r=0.0)
        await show_menu(callback, state)


@router.message(ContourWizard.size)
async def input_size(message: Message, state: FSMContext) -> None:
    try:
        x, y, z = map(float, message.text.replace(",", ".").split())
        if x <= 0 or y <= 0 or z <= 0 or x > 1350 or y > 700 or z > 500:
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


async def generate(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    try:
        program = build_contour_program(data)
    except (ValueError, TypeError, KeyError) as exc:
        await callback.answer(str(exc)[:180], show_alert=True)
        return

    await callback.message.answer_document(
        BufferedInputFile(program.encode("utf-8"), filename="contour_fanuc.nc"),
        caption=(
            "Черновая УП создана. Проверьте геометрию, ноль XY/Z, корректор H, "
            "вылет, крепление заготовки и пределы перемещений в симуляторе. "
            "Подача по Z вертикальная; перед станком подтвердите допустимость врезания "
            "для выбранного инструмента и материала."
        ),
    )
    await callback.answer("G-код сформирован.")
