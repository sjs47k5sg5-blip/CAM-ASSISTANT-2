from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from .cam_router import show_milling_menu

router = Router()


# =========================
# MAIN MENU (ReplyKeyboard)
# =========================

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📐 Фрезерование")],
        [KeyboardButton(text="🕳 Отверстия")],
        [KeyboardButton(text="📚 Справочник")],
        [KeyboardButton(text="⚙️ Утилиты")]
    ],
    resize_keyboard=True
)


# =========================
# START
# =========================

@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "👋 Добро пожаловать в CAM Assistant Pro!",
        reply_markup=main_menu
    )


# =========================
# ENTER MILLING MENU
# =========================

@router.message(F.text == "📐 Фрезерование")
async def milling_menu(message: Message):

    await show_milling_menu(message)