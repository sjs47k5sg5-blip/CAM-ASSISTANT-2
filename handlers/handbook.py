from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "📚 Пособие")
async def handbook(message: Message):

    await message.answer(

        "📚 Раздел находится в разработке."

    )