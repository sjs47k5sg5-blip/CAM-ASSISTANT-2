from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "📚 Пособие")
async def handbook(message: Message):

    await message.answer(
        "📚 СПРАВОЧНИК\n\n"
        "Раздел находится в разработке.\n\n"
        "Будут добавлены:\n"
        "• G-коды\n"
        "• M-коды\n"
        "• Допуски и посадки\n"
        "• Режимы резания\n"
        "• Материалы\n"
        "• Таблицы сверл\n"
        "• Резьбы"
    )