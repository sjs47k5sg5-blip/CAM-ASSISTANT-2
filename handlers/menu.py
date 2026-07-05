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
        "🚀 CAM CORE READY\nВыберите операцию:",
        reply_markup=cam_menu
    )


# =========================
# OPEN CAM MENU
# =========================
@router.message(F.text == "CAM")
async def open_cam(message: Message):
    await message.answer(
        "📐 CAM модуль открыт\nВыберите операцию:",
        reply_markup=cam_menu
    )


# =========================
# BUTTONS
# =========================
@router.message(F.text == "Контур")
async def contour(message: Message):
    await message.answer("📐 Контур выбран")


@router.message(F.text == "Карман")
async def pocket(message: Message):
    await message.answer("🟦 Карман выбран")


@router.message(F.text == "Утилиты")
async def utils(message: Message):
    await message.answer("⚙️ Утилиты открыты")


@router.message(F.text == "Справочник")
async def manual(message: Message):
    await message.answer("📚 Справочник открыт")


@router.message(F.text == "Назад")
async def back(message: Message):
    await message.answer("🔙 Возврат в меню", reply_markup=cam_menu)