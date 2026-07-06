from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "🕳 Обработка отверстий")
async def holes(message: Message):

    await message.answer(
        "🕳 ОБРАБОТКА ОТВЕРСТИЙ\n\n"
        "Раздел находится в разработке.\n\n"
        "В следующих версиях будут:\n"
        "• Сверление\n"
        "• Зенковка\n"
        "• Развертывание\n"
        "• Нарезание резьбы"
    )