from aiogram import Router, F
from aiogram.types import Message
from keyboards.cam_menu import cam_menu

router = Router()

@router.message(F.text == "CAM")
async def cam(message: Message):
    await message.answer("МЕНЮ CAM v8", reply_markup=cam_menu)
