from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "🕳 Обработка отверстий")
async def holes(message: Message):
    await message.answer(
        "🕳 ОТВЕРСТИЯ\n\n"
        "• Сверление\n"
        "• Зенковка\n"
        "• Резьба"
    )