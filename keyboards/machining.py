from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton

machining_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Черновая")],
        [KeyboardButton(text="Получистовая")],
        [KeyboardButton(text="Чистовая")]
    ],
    resize_keyboard=True
)