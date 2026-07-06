from aiogram import Router, F
from aiogram.types import Message

from keyboards.main_menu import main_menu
from keyboards.cam_wizard import wizard_type

router = Router()


@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "🚀 CAM SYSTEM READY",
        reply_markup=main_menu()
    )


@router.message(F.text == "⚙ Фрезерные операции")
async def cam_entry(message: Message):
    await message.answer(
        "⚙ CAM WIZARD START",
        reply_markup=wizard_type()
    )


@router.message(F.text == "ℹ О программе")
async def about(message: Message):
    await message.answer("CAM Assistant v3 CLEAN CORE")