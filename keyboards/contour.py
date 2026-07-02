from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

contour_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬜ Наружный"),
            KeyboardButton(text="🔲 Внутренний"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
)