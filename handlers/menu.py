from __future__ import annotations

import math

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

router = Router()


class Calculator(StatesGroup):
    drilling = State()
    thread = State()
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


@router.message(F.text.in_({"/start", "/menu", "⬅ В меню"}))
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "🤖 <b>CAM Assistant</b>\n\n"
        "Выберите операцию. Программы ЧПУ перед запуском обязательно проверяйте в симуляторе и на станке.",
        reply_markup=main_menu(),
    )


@router.message(F.text == "ℹ О программе")
async def about(message: Message) -> None:
    await message.answer(
        "<b>CAM Assistant</b>\n"
        "Помощник наладчика ЧПУ: расчёт сверления, резьбы, режимов резания и генерация контура Fanuc."
    )


@router.message(F.text == "📚 Справочник")
async def handbook(message: Message) -> None:
    await message.answer(
        "<b>Краткий справочник</b>\n"
        "G00 — быстрый ход; G01 — линейная подача; G02/G03 — дуга; G17 — плоскость XY; "
        "G21 — миллиметры; G40 — отмена коррекции; G43 — коррекция длины; G54 — рабочая система; "
        "M03 — шпиндель по часовой; M08/M09 — СОЖ вкл./выкл.; M30 — конец программы."
    )


@router.message(F.text == "🕳 Сверление")
async def drilling_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Calculator.drilling)
    await message.answer(
        "Введите через пробел: <b>диаметр глубина число_отверстий обороты подача</b>\n"
        "Пример: <code>8 20 4 1500 120</code>\n"
        "Подача — мм/мин. Значения оборотов и подачи проверьте по инструменту и материалу."
    )


@router.message(Calculator.drilling)
async def drilling_input(message: Message, state: FSMContext) -> None:
    try:
        d, depth, count, rpm, feed = map(float, message.text.replace(",", ".").split())
        if min(d, depth, count, rpm, feed) <= 0 or not count.is_integer() or rpm > 15000:
            raise ValueError
    except (ValueError, AttributeError):
        await message.answer("Неверный ввод. Пример: <code>8 20 4 1500 120</code>")
        return
    await state.clear()
    await message.answer(
        f"<b>Параметры сверления</b>\nØ{d:g} мм, глубина {depth:g} мм, отверстий {int(count)}, "
        f"S{int(rpm)} об/мин, F{feed:g} мм/мин.\n\n"
        "Для FANUC используйте цикл G81/G83 только после выбора координат отверстий, плоскости отвода "
        "и безопасной глубины. Автоматическую УП без координат отверстий бот не создаёт.",
        reply_markup=main_menu(),
    )


@router.message(F.text == "🧵 Резьба")
async def thread_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Calculator.thread)
    await message.answer(
        "Введите: <b>диаметр шаг глубина обороты</b>\nПример: <code>10 1.5 15 500</code>\n"
        "Расчёт для метрической резьбы и цикла G84."
    )


@router.message(Calculator.thread)
async def thread_input(message: Message, state: FSMContext) -> None:
    try:
        diameter, pitch, depth, rpm = map(float, message.text.replace(",", ".").split())
        if min(diameter, pitch, depth, rpm) <= 0 or rpm > 15000:
            raise ValueError
    except (ValueError, AttributeError):
        await message.answer("Неверный ввод. Пример: <code>10 1.5 15 500</code>")
        return
    feed = rpm * pitch
    await state.clear()
    await message.answer(
        f"<b>Резьба M{diameter:g}×{pitch:g}</b>\n"
        f"Глубина: {depth:g} мм\nS{rpm:g} об/мин\n"
        f"F = S × P = <b>{feed:g} мм/мин</b>\n\n"
        "Фрагмент цикла (добавьте координаты отверстия и плоскость отвода):\n"
        f"<code>G84 Z-{depth:g} R2. F{feed:g}</code>\n"
        "Проверьте направление резьбы, компенсацию синхронизации и параметры метчика.",
        reply_markup=main_menu(),
    )


@router.message(F.text == "⚙ Режимы резания")
async def cutting_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Calculator.cutting)
    await message.answer(
        "Введите: <b>диаметр фрезы число_зубьев Vc fz</b>\n"
        "Пример: <code>10 4 120 0.03</code>\n"
        "Vc — м/мин, fz — мм/зуб. Это расчётная оценка, не готовая рекомендация для любого материала."
    )


@router.message(Calculator.cutting)
async def cutting_input(message: Message, state: FSMContext) -> None:
    try:
        diameter, teeth, vc, fz = map(float, message.text.replace(",", ".").split())
        if min(diameter, teeth, vc, fz) <= 0:
            raise ValueError
    except (ValueError, AttributeError):
        await message.answer("Неверный ввод. Пример: <code>10 4 120 0.03</code>")
        return
    rpm = min(15000, (1000 * vc) / (math.pi * diameter))
    feed = rpm * teeth * fz
    await state.clear()
    await message.answer(
        f"<b>Расчёт режимов</b>\nS ≈ <b>{rpm:.0f} об/мин</b>\n"
        f"F ≈ <b>{feed:.0f} мм/мин</b>\n"
        "Учитывайте материал, тип фрезы, вылет, жёсткость системы и рекомендации производителя.",
        reply_markup=main_menu(),
    )


@router.message(F.text)
async def unknown(message: Message) -> None:
    await message.answer("Не понял команду. Нажмите /start и выберите раздел в меню.")
