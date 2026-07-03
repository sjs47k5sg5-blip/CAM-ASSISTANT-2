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
            KeyboardButton(text="h5"),
            KeyboardButton(text="h6"),
            KeyboardButton(text="h7"),
        ],
        [
            KeyboardButton(text="h8"),
            KeyboardButton(text="h9"),
            KeyboardButton(text="h10"),
        ],
        [
            KeyboardButton(text="h11"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
)