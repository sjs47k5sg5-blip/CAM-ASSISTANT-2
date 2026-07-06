from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "ℹ О программе")
async def about(message: Message):

    await message.answer(
        "CAM Assistant\n\n"
        "Версия: V4 Development\n\n"
        "Функции:\n"
        "• Генерация G-кода\n"
        "• Контурная обработка\n"
        "• CAM Wizard\n\n"
        "Разработка продолжается."
    )