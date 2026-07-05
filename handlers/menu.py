from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

# =========================
# MAIN MENU
# =========================
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📐 Контур")],
            [KeyboardButton(text="📘 Справочник")]
        ],
        resize_keyboard=True
    )


# =========================
# START (LOCKED)
# =========================
@router.message(F.text == "/start")
async def start(message: Message):

    await message.answer(
        "🚀 CAM PRO READY\nВыберите функцию:",
        reply_markup=main_menu()
    )


# =========================
# SAFETY: ignore CAM echo duplicates
# =========================
@router.message(F.text.in_(["CAM PRO READY", "CAM модуль активирован"]))
async def ignore_duplicates(message: Message):
    return