from aiogram import Router, F
from aiogram.types import Message
from keyboards.cam_menu import cam_menu

router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer("🚀 CAM PRO V6 READY", reply_markup=cam_menu)
