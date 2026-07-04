from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

finish_modes_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅ Использовать те же режимы"),
        ],
        [
            KeyboardButton(text="✏️ Изменить режимы"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
)