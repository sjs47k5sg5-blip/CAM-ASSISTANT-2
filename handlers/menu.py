from aiogram import Router, F
from aiogram.types import Message

from keyboards.main_menu import main_menu
from keyboards.cam_wizard import wizard_type

router = Router()


# =========================
# START
# =========================
@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "CAM SYSTEM READY",
        reply_markup=main_menu()
    )


# =========================
# PROJECT
# =========================
@router.message(F.text == "📁 Проект")
async def project(message: Message):
    await message.answer("📁 Проекты (в разработке)")


# =========================
# CAM ENTRY → WIZARD
# =========================
@router.message(F.text == "⚙ Фрезерные операции")
async def milling(message: Message):
    await message.answer(
        "⚙ CAM MODULE\nВыберите операцию:",
        reply_markup=wizard_type()
    )


# =========================
# HOLES (future)
# =========================
@router.message(F.text == "🕳 Обработка отверстий")
async def holes(message: Message):
    await message.answer("🕳 Отверстия (в разработке)")


# =========================
# REFERENCE (future)
# =========================
@router.message(F.text == "📚 Справочник")
async def reference(message: Message):
    await message.answer("📚 Справочник (в разработке)")


# =========================
# ABOUT
# =========================
@router.message(F.text == "ℹ О программе")
async def about(message: Message):
    await message.answer(
        "CAM Assistant\nFanuc-style G-code generator"
    )