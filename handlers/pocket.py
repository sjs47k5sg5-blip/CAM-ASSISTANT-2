from __future__ import annotations

import math

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    BufferedInputFile, CallbackQuery, InlineKeyboardButton,
    InlineKeyboardMarkup, Message,
)

from services.cam_engine.pocket import build_pocket_program

router = Router()


class PocketWizard(StatesGroup):
    size = State()
    zero_xy = State()
    zero_z = State()
    tool = State()
    step = State()
    feeds = State()


def choices(rows: list[list[tuple[str, str]]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=label, callback_data=data) for label, data in row]
        for row in rows
    ])


def summary(data: dict) -> str:
    return (
        "<b>🧱 Прямоугольный карман</b>\n"
        f"Размер: {data.get('x', '—')} × {data.get('y', '—')} мм\n"
        f"Глубина: {data.get('depth', '—')} мм\n"
        f"Ноль XY: {data.get('zero', '—')} | Ноль Z: {data.get('zero_z', '—')}\n"
        f"Инструмент: T{data.get('tool', '—')} Ø{data.get('tool_d', '—')} мм\n"
        f"Шаг Z: {data.get('step_z', '—')} мм | Боковой шаг: {data.get('stepover', '—')}% Ø\n"
        f"Припуск стенки: {data.get('allowance', '—')} мм\n"
        f"S: {data.get('rpm', '—')} об/мин | F: {data.get('feed', '—')} мм/мин"
    )


@router.message(F.text == "🧱 Карман")
async def start_pocket(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(PocketWizard.size)
    await message.answer(
        "<b>Мастер кармана</b>\nВведите X Y глубину в мм.\n"
        "Пример: <code>100 80 12</code>\n"
        "Генерируется прямоугольный карман с растровой черновой обработкой, "
        "чистовым проходом по дну и стенкам."
    )


@router.message(PocketWizard.size)
async def pocket_size(message: Message, state: FSMContext) -> None:
    try:
        x, y, depth = map(float, message.text.replace(",", ".").split())
        if not all(math.isfinite(v) for v in (x, y, depth)):
            raise ValueError
        if min(x, y, depth) <= 0 or x > 1350 or y > 700 or depth > 500:
            raise ValueError
    except (ValueError, AttributeError):
        await message.answer("Введите три положительных числа в пределах станка. Пример: <code>100 80 12</code>")
        return
    await state.update_data(x=x, y=y, depth=depth)
    await state.set_state(PocketWizard.zero_xy)
    await message.answer(
        "Выберите положение нуля XY:",
        reply_markup=choices([
            [("Центр", "pocket:xy:CENTER")],
            [("Левый нижний", "pocket:xy:BL"), ("Правый нижний", "pocket:xy:BR")],
            [("Левый верхний", "pocket:xy:TL"), ("Правый верхний", "pocket:xy:TR")],
        ]),
    )


@router.callback_query(F.data.startswith("pocket:xy:"))
async def pocket_zero_xy(callback: CallbackQuery, state: FSMContext) -> None:
    value = callback.data.rsplit(":", 1)[1]
    await state.update_data(zero=value)
    await state.set_state(PocketWizard.zero_z)
    await callback.message.edit_text(
        "Выберите положение нуля Z:",
        reply_markup=choices([
            [("Верх детали", "pocket:z:TOP")],
            [("Низ детали", "pocket:z:BOTTOM")],
        ]),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("pocket:z:"))
async def pocket_zero_z(callback: CallbackQuery, state: FSMContext) -> None:
    value = callback.data.rsplit(":", 1)[1]
    await state.update_data(zero_z=value)
    await state.set_state(PocketWizard.tool)
    await callback.message.answer(
        "Введите номер инструмента и диаметр фрезы.\nПример: <code>5 10</code>"
    )
    await callback.answer()


@router.message(PocketWizard.tool)
async def pocket_tool(message: Message, state: FSMContext) -> None:
    try:
        tool_s, diameter_s = message.text.replace(",", ".").split()
        tool, diameter = int(tool_s), float(diameter_s)
        if not math.isfinite(diameter) or not 1 <= tool <= 30 or diameter <= 0 or diameter > 100:
            raise ValueError
    except (ValueError, AttributeError):
        await message.answer("Формат: номер инструмента и диаметр. Пример: <code>5 10</code>")
        return
    await state.update_data(tool=tool, tool_d=diameter)
    await state.set_state(PocketWizard.step)
    await message.answer(
        "Введите шаг по Z, боковой шаг в процентах диаметра и припуск на стенку в мм.\n"
        "Пример: <code>2 40 0.2</code>\n"
        "Боковой шаг: 5–80% диаметра."
    )


@router.message(PocketWizard.step)
async def pocket_step(message: Message, state: FSMContext) -> None:
    try:
        step_z, stepover, allowance = map(float, message.text.replace(",", ".").split())
        if not all(math.isfinite(v) for v in (step_z, stepover, allowance)):
            raise ValueError
        if not 0 < step_z <= 10 or not 5 <= stepover <= 80 or not 0 <= allowance <= 5:
            raise ValueError
    except (ValueError, AttributeError):
        await message.answer("Пример: <code>2 40 0.2</code>. Шаг Z до 10 мм, боковой 5–80%, припуск 0–5 мм.")
        return
    await state.update_data(step_z=step_z, stepover=stepover, allowance=allowance)
    await state.set_state(PocketWizard.feeds)
    await message.answer("Введите обороты шпинделя и подачу мм/мин. Пример: <code>1500 150</code>")


@router.message(PocketWizard.feeds)
async def pocket_feeds(message: Message, state: FSMContext) -> None:
    try:
        rpm_s, feed_s = message.text.replace(",", ".").split()
        rpm, feed = int(rpm_s), float(feed_s)
        if not math.isfinite(feed) or not 100 <= rpm <= 15000 or not 1 <= feed <= 15000:
            raise ValueError
    except (ValueError, AttributeError):
        await message.answer("Обороты 100–15000, подача 1–15000. Пример: <code>1500 150</code>")
        return
    await state.update_data(rpm=rpm, feed=feed)
    data = await state.get_data()
    await state.set_state(None)
    await message.answer(
        summary(data) + "\n\nПроверьте параметры и подтвердите генерацию:",
        reply_markup=choices([
            [("✅ Создать УП кармана", "pocket:generate")],
            [("❌ Отмена", "pocket:cancel")],
        ]),
    )


@router.callback_query(F.data == "pocket:generate")
async def pocket_generate(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    try:
        program = build_pocket_program(data)
    except (ValueError, TypeError, KeyError) as exc:
        await callback.answer(str(exc)[:180], show_alert=True)
        return
    await callback.message.answer_document(
        BufferedInputFile(program.encode("utf-8"), filename="pocket_fanuc.nc"),
        caption=(
            "УП прямоугольного кармана сформирована. До запуска обязательно проверьте "
            "траекторию в симуляторе: G54, H-корректор, Z0, габариты, зажим, вылет и "
            "допустимость рампового врезания для конкретной фрезы и материала. "
            "Постпроцессор рассчитан на проверку наладчиком, а не на безусловный запуск."
        ),
    )
    await state.clear()
    await callback.answer("Файл создан.")


@router.callback_query(F.data == "pocket:cancel")
async def pocket_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.answer("Создание кармана отменено. Нажмите /start для главного меню.")
    await callback.answer()
