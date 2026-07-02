from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

direction_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➡️ Попутное"),
        ],
        [
            KeyboardButton(text="⬅️ Встречное"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
)