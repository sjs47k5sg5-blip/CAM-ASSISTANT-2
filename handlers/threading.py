from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import ThreadState

from services.threading import (
    get_thread,
    spindle_speed,
    feed_rate,
    tapping_cycle,
    tapping_time,
)

from keyboards.main_menu import main_menu

router = Router()


THREADS = [
    "M3",
    "M4",
    "M5",
    "M6",
    "M8",
    "M10",
    "M12",
]


@router.message(F.text == "🔩 Нарезание резьбы")
async def thread_start(message: Message, state: FSMContext):

    await state.clear()

    await state.set_state(ThreadState.thread)

    await message.answer(
        "Введите резьбу (например M6):"
    )


@router.message(ThreadState.thread)
async def thread_selected(message: Message, state: FSMContext):

    thread = message.text.upper()

    if thread not in THREADS:
        await message.answer(
            "Неизвестная резьба.\n\nНапример: M3 M4 M5 M6 M8 M10 M12"
        )
        return

    await state.update_data(thread=thread)

    await state.set_state(ThreadState.depth)

    await message.answer(
        "Введите глубину резьбы (мм):"
    )


@router.message(ThreadState.depth)
async def thread_depth(message: Message, state: FSMContext):

    try:
        depth = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите число.")
        return

    data = await state.get_data()

    thread = data["thread"]

    info = get_thread(thread)

    drill = info["drill"]
    pitch = info["pitch"]

    rpm = spindle_speed(thread)

    feed = feed_rate(rpm, pitch)

    cycle = tapping_cycle(True)

    time_sec = tapping_time(depth, feed)

    await message.answer(
        f"""
🔩 НАРЕЗАНИЕ РЕЗЬБЫ

Резьба:
{thread}

Диаметр сверления:
Ø{drill}

Шаг:
{pitch}

────────────────

Обороты

S{rpm}

Подача

F{feed}

────────────────

Цикл

{cycle}

────────────────

Время

≈ {time_sec} сек
""",
        reply_markup=main_menu,
    )

    await state.clear()