from aiogram import Router, F
from aiogram.types import Message

from keyboards.reference import reference_keyboard
from keyboards.thread_reference import thread_reference_keyboard
from keyboards.main_menu import main_menu

router = Router()


@router.message(F.text == "📚 Справочник")
async def reference_menu(message: Message):
    await message.answer(
        "📚 Выберите раздел справочника",
        reply_markup=reference_keyboard,
    )


@router.message(F.text == "🔩 Резьбы")
async def thread_reference(message: Message):
    await message.answer(
        "Выберите размер резьбы",
        reply_markup=thread_reference_keyboard,
    )


THREADS = {
    "M3": "🔩 M3\n\nШаг: 0.5\nСверло: Ø2.5",
    "M4": "🔩 M4\n\nШаг: 0.7\nСверло: Ø3.3",
    "M5": "🔩 M5\n\nШаг: 0.8\nСверло: Ø4.2",
    "M6": "🔩 M6\n\nШаг: 1.0\nСверло: Ø5.0",
    "M8": "🔩 M8\n\nШаг: 1.25\nСверло: Ø6.8",
    "M10": "🔩 M10\n\nШаг: 1.5\nСверло: Ø8.5",
    "M12": "🔩 M12\n\nШаг: 1.75\nСверло: Ø10.2",
    "M16": "🔩 M16\n\nШаг: 2.0\nСверло: Ø14.0",
    "M20": "🔩 M20\n\nШаг: 2.5\nСверло: Ø17.5",
}


@router.message(F.text.in_(THREADS.keys()))
async def show_thread(message: Message):
    await message.answer(THREADS[message.text])


@router.message(F.text == "⬅️ Назад")
async def back(message: Message):
    await message.answer(
        "🏠 Главное меню",
        reply_markup=main_menu,
    )