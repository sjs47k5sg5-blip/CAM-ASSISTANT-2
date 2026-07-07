from aiogram import Router, F
from aiogram.types import Message

from keyboards.drilling_menu import drilling_menu

router = Router()


@router.message(F.text == "🕳 Обработка отверстий")
async def holes(message: Message):

    await message.answer(

        "🕳 Выберите операцию.",

        reply_markup=drilling_menu()

    )