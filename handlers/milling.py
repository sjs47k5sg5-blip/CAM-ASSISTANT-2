from aiogram import Router, F
from aiogram.types import Message

from keyboards.milling_menu import milling_menu

router = Router()


@router.message(F.text == "⚙ Фрезерная обработка")
async def milling(message: Message):

    await message.answer(
        "Выберите операцию",
        reply_markup=milling_menu()
    )