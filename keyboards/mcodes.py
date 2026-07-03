from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

mcodes_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="M00"),
            KeyboardButton(text="M01"),
            KeyboardButton(text="M03"),
            KeyboardButton(text="M04"),
        ],
        [
            KeyboardButton(text="M05"),
            KeyboardButton(text="M06"),
            KeyboardButton(text="M08"),
            KeyboardButton(text="M09"),
        ],
        [
            KeyboardButton(text="M19"),
            KeyboardButton(text="M30"),
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
)