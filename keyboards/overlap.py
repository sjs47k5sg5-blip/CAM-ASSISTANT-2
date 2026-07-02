from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

overlap_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="20%"),
            KeyboardButton(text="30%"),
            KeyboardButton(text="40%"),
        ],
        [
            KeyboardButton(text="50%"),
            KeyboardButton(text="60%"),
            KeyboardButton(text="70%"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
)