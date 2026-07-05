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
# OPEN CAM MENU
# =========================
@router.message(F.text == "CAM")
async def open_cam(message: Message):
    await message.answer(
        "📐 CAM модуль открыт\nВыберите операцию:",
        reply_markup=cam_menu
    )


# =========================
# CONTROLLERS (ТОЛЬКО UI)
# =========================
@router.message(F.text == "Контур")
async def contour_btn(message: Message):
    await message.answer("📐 Контур выбран")


@router.message(F.text == "Карман")
async def pocket_btn(message: Message):
    await message.answer("🟦 Карман выбран")


@router.message(F.text == "Утилиты")
async def utils_btn(message: Message):
    await message.answer("⚙️ Утилиты")


@router.message(F.text == "Справочник")
async def manual_btn(message: Message):
    await message.answer("📚 Справочник")


@router.message(F.text == "Назад")
async def back_btn(message: Message):
    await message.answer("🔙 Главное меню", reply_markup=cam_menu)