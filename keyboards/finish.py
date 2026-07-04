from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

finish_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅ Да"),
            KeyboardButton(text="❌ Нет"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
)