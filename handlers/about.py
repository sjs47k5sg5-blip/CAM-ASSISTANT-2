from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "ℹ О программе")
async def about(message: Message):

    await message.answer(

        "🤖 CAM Assistant V5\n\n"
        "Промышленный CAM для станков с ЧПУ.\n\n"
        "Версия: 5.0"

    )