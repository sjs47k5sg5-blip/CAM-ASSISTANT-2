from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()


# =========================
# MAIN MENU KEYBOARD
# =========================
def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📐 Контур")],
            [KeyboardButton(text="📘 Справочник")]
        ],
        resize_keyboard=True
    )


# =========================
# START COMMAND (FIXED)
# =========================
@router.message(F.text == "/start")
async def start(message: Message):

    await message.answer(
        "🚀 CAM PRO READY\n\nВыберите функцию из меню ниже:",
        reply_markup=main_menu_kb()
    )


# =========================
# BACKUP ENTRY (если пользователь пишет CAM)
# =========================
@router.message(F.text.in_(["CAM", "cam", "📐 Контур"]))
async def open_cam(message: Message):

    await message.answer(
        "📐 CAM модуль активирован\nИспользуйте кнопку Контур ниже",
        reply_markup=main_menu_kb()
    )