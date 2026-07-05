from aiogram import Router, F
from aiogram.types import Message
from keyboards.cam_menu import cam_menu

router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer("🚀 CAM CORE FINAL (MERGED)", reply_markup=cam_menu)
