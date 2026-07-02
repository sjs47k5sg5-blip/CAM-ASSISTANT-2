from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton

materials_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сталь 20")],
        [KeyboardButton(text="Сталь 45")],
        [KeyboardButton(text="40Х")],
        [KeyboardButton(text="Нержавейка")],
        [KeyboardButton(text="Чугун")],
        [KeyboardButton(text="D16")],
        [KeyboardButton(text="АМг6")],
        [KeyboardButton(text="Латунь")]
    ],
    resize_keyboard=True
)