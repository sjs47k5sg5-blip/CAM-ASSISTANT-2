from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import main_menu

router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer("🚀 CAM CORE v7 PRO READY", reply_markup=main_menu)
