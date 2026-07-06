from aiogram import Router, F
from aiogram.types import Message

from keyboards.main_menu import main_menu
from keyboards.cam_menu import milling_menu

router = Router()


@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer("🚀 CAM SYSTEM READY", reply_markup=main_menu())


@router.message(F.text == "⚙ Фрезерная обработка")
async def milling(message: Message):
    await message.answer(
        "⚙ ФРЕЗЕРОВКА",
        reply_markup=milling_menu()   # 🔥 ВАЖНО: ВОТ ЭТО КНОПКИ
    )