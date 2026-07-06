from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "📁 Проекты")
async def projects(message: Message):
    await message.answer(
        "📁 ПРОЕКТЫ\n\n"
        "• Создать проект\n"
        "• Открыть проект\n"
        "• Сохранение параметров"
    )