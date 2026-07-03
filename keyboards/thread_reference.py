from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

thread_reference_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="M3"),
            KeyboardButton(text="M4"),
            KeyboardButton(text="M5"),
        ],
        [
            KeyboardButton(text="M6"),
            KeyboardButton(text="M8"),
            KeyboardButton(text="M10"),
        ],
        [
            KeyboardButton(text="M12"),
            KeyboardButton(text="M16"),
            KeyboardButton(text="M20"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
)