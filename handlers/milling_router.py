from aiogram import Router, F
from aiogram.types import Message
from keyboards.milling_kb import milling_kb

router = Router()

@router.message(F.text == "Фрезерование")
async def milling_menu(message: Message):
    await message.answer(
        "Выберите операцию:",
        reply_markup=milling_kb
    )