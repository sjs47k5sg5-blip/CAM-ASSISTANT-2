from aiogram import Router, F
from aiogram.types import Message

from keyboards.milling import milling_keyboard
from keyboards.holes import holes_keyboard
from keyboards.reference import reference_keyboard
from keyboards.utils import utils_keyboard

router = Router()


@router.message(F.text == "📐 Фрезерование")
async def milling_menu(message: Message):
    await message.answer(
        "📐 Выберите раздел фрезерования",
        reply_markup=milling_keyboard,
    )


@router.message(F.text == "🕳 Отверстия")
async def holes_menu(message: Message):
    await message.answer(
        "🕳 Выберите операцию",
        reply_markup=holes_keyboard,
    )


@router.message(F.text == "📚 Справочник")
async def reference_menu(message: Message):
    await message.answer(
        "📚 Выберите раздел",
        reply_markup=reference_keyboard,
    )


@router.message(F.text == "⚙️ Утилиты")
async def utils_menu(message: Message):
    await message.answer(
        "⚙️ Выберите утилиту",
        reply_markup=utils_keyboard,
    )