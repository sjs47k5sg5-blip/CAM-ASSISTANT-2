from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📐 Фрезерование")],
        [KeyboardButton(text="🕳 Отверстия")],
        [KeyboardButton(text="📚 Справочник")],
        [KeyboardButton(text="⚙️ Утилиты")]
    ],
    resize_keyboard=True
)