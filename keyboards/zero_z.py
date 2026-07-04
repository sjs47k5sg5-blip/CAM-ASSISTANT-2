from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

zero_z_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬆️ Верх детали"),
        ],
        [
            KeyboardButton(text="⬇️ Низ детали"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
)