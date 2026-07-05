
from aiogram import Router, F
from aiogram.types import Message
from keyboards.cam_keyboard import cam_keyboard

router = Router()

@router.message(F.text == "CAM")
async def cam(message: Message):
    await message.answer("CAM MENU", reply_markup=cam_keyboard)
