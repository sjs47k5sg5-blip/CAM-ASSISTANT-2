from aiogram import Router, F
from aiogram.types import Message

from keyboards.main_menu import main_menu

router = Router()


@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer("🚀 CAM SYSTEM READY", reply_markup=main_menu())


@router.message(F.text == "📁 Проект")
async def project(message: Message):
    await message.answer("📁 Проект (future)")


@router.message(F.text == "⚙ Фрезерные операции")
async def cam(message: Message):
    await message.answer("📐 Открыт CAM → нажмите Контур")


@router.message(F.text == "🕳 Обработка отверстий")
async def holes(message: Message):
    await message.answer("🕳 Module (future)")


@router.message(F.text == "ℹ О программе")
async def about(message: Message):
    await message.answer("CAM Assistant V1 FIX")