from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "📚 Пособие")
async def manual(message: Message):
    await message.answer(
        "📚 ПОСОБИЕ\n\n"
        "G0 - быстрый ход\n"
        "G1 - линейное движение\n"
        "G2/G3 - дуги\n\n"
        "M3 - шпиндель\n"
        "M5 - стоп\n\n"
        "H7 / H8 / H9 / H11 - посадки"
    )