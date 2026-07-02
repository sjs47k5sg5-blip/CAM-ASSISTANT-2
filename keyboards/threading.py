from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

thread_keyboard = ReplyKeyboardMarkup(
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
            KeyboardButton(text="M14"),
            KeyboardButton(text="M16"),
        ],
        [
            KeyboardButton(text="M18"),
            KeyboardButton(text="M20"),
            KeyboardButton(text="M22"),
        ],
        [
            KeyboardButton(text="M24"),
            KeyboardButton(text="M27"),
            KeyboardButton(text="M30"),
        ],
        [
            KeyboardButton(text="⬅️ Назад")
        ]
    ],
    resize_keyboard=True
)