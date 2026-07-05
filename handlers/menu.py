from aiogram import Router, F
from aiogram.types import Message

from keyboards.cam_menu import cam_menu

router = Router()

# =========================
# START
# =========================
@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "🚀 CAM CORE READY\nВыберите модуль:",
        reply_markup=cam_menu
    )


# =========================
# OPEN CAM (если нажали CAM кнопку отдельно)
# =========================
@router.message(F.text == "CAM")
async def open_cam(message: Message):
    await message.answer(
        "📐 CAM модуль открыт",
        reply_markup=cam_menu
    )


# =========================
# SAFE FALLBACK (НЕ ЛОМАЕТ CAM)
# =========================
@router.message(
    ~F.text.in_([
        "/start",
        "CAM",
        "Контур",
        "Карман",
        "Утилиты",
        "Справочник",
        "Назад"
    ])
)
async def fallback(message: Message):
    await message.answer("⚠️ Используйте кнопки меню /start")