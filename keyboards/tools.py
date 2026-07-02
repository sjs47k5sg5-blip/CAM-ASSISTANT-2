from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

tools_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Твердосплавная")],
        [KeyboardButton(text="HSS")]
    ],
    resize_keyboard=True
)