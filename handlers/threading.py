from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from states import ThreadState

from services.threading import (
    get_thread,
    feed_rate,
    tapping_cycle,
    tapping_time,
)

from services.thread_gcode import threading_gcode

from keyboards.threading import thread_keyboard
from keyboards.main_menu import main_menu

router = Router()


@router.message(F.text == "🔩 Нарезание резьбы")
async def thread_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ThreadState.thread)

    await message.answer(
        "🔩 Выберите резьбу",
        reply_markup=thread_keyboard,
    )


@router.message(ThreadState.thread)
async def thread_selected(message: Message, state: FSMContext):

    thread = message.text.upper()

    try:
        get_thread(thread)
    except KeyError:
        await message.answer(
            "Выберите резьбу кнопками.",
            reply_markup=thread_keyboard,
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

    await state.update_data(depth=depth)

    await state.set_state(ThreadState.rpm)

    await message.answer(
        "Введите обороты шпинделя S (об/мин):"
    )


@router.message(ThreadState.rpm)
async def thread_rpm(message: Message, state: FSMContext):

    try:
        rpm = int(message.text)
    except ValueError:
        await message.answer("Введите целое число.")
        return

    data = await state.get_data()

    thread = data["thread"]
    depth = data["depth"]

    info = get_thread(thread)

    drill = info["drill"]
    pitch = info["pitch"]

    feed = feed_rate(rpm, pitch)

    cycle = tapping_cycle(True)

    time_sec = tapping_time(depth, feed)

    gcode = threading_gcode(
        tool=1,
        rpm=rpm,
        feed=feed,
        depth=depth,
    )

    filename = f"THREAD_{thread}.nc"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(gcode)

    await message.answer(
        f"""
🔩 НАРЕЗАНИЕ РЕЗЬБЫ

Резьба:
{thread}

Диаметр сверления:
Ø{drill:.1f} мм

Шаг:
{pitch:.2f} мм

────────────────

Обороты

S{rpm}

Подача

F{feed}

────────────────

Команды Fanuc

M29

{cycle}

────────────────

Время обработки

≈ {time_sec} сек

────────────────

Пример G-кода

<pre>{gcode}</pre>
""",
        parse_mode="HTML",
        reply_markup=main_menu,
    )

    await message.answer_document(
        FSInputFile(filename),
        caption=f"📄 G-код для резьбы {thread}"
    )

    await state.clear()