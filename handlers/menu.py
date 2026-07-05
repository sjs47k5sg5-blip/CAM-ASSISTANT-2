from aiogram import Router, F
from aiogram.types import Message
from keyboards.cam_menu import cam_menu

router = Router()

# =========================
# START MENU
# =========================
@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "🚀 CAM CORE READY\nВыберите модуль:",
        reply_markup=cam_menu
    )


# =========================
# MAIN CAM BUTTON
# =========================
@router.message(F.text == "📐 CAM")
async def cam_open(message: Message):
    await message.answer(
        "📐 CAM модуль открыт\nВыберите операцию:",
        reply_markup=cam_menu
    )


# =========================
# SAFE FALLBACK
# =========================
@router.message()
async def fallback(message: Message):
    # чтобы бот не "зависал" на непонятных сообщениях
    await message.answer("⚠️ Используйте кнопки меню /start")