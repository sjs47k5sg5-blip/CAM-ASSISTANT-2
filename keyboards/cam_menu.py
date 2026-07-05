from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cam_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📐 Контур"), KeyboardButton(text="🟦 Карман")],
        [KeyboardButton(text="📚 Справочник"), KeyboardButton(text="⚙️ Утилиты")],
    ],
    resize_keyboard=True
)