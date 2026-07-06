from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "ℹ О программе")
async def about(message: Message):
    await message.answer(
        "CAM Assistant V1 FINAL\n"
        "Status: ACTIVE\n"
        "Engine: CUSTOM CAM CORE"
    )