from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton

catalog_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Sandvik")],
        [KeyboardButton(text="ISCAR")],
        [KeyboardButton(text="Mitsubishi")]
    ],
    resize_keyboard=True
)