from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

tolerances_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="H6"),
            KeyboardButton(text="H7"),
            KeyboardButton(text="H8"),
        ],
        [
            KeyboardButton(text="H9"),
            KeyboardButton(text="H10"),
            KeyboardButton(text="H11"),
        ],
        [
            KeyboardButton(text="H12"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
)