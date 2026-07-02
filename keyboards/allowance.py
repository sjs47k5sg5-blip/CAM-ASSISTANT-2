from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

allowance_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="0"),
            KeyboardButton(text="0.2"),
            KeyboardButton(text="0.5"),
        ],
        [
            KeyboardButton(text="1.0"),
            KeyboardButton(text="2.0"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
)