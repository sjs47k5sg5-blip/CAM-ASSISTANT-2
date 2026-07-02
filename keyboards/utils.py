from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

utils_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📄 Генерация G-кода"),
        ],
        [
            KeyboardButton(text="📊 Калькуляторы"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
)