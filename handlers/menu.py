from aiogram import Router, F
from aiogram.types import Message
from keyboards.cam_menu import cam_menu

router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "🚀 CAM CORE READY\nВыберите операцию:",
        reply_markup=cam_menu
    )

@router.message(F.text == "📚 Справочник")
async def manual(message: Message):
    await message.answer("📚 Справочник открыт")

@router.message(F.text == "⚙️ Утилиты")
async def utils(message: Message):
    await message.answer("⚙️ Утилиты открыты")