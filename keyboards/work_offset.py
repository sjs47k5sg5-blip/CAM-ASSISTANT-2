from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

work_offset_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="G54"),
            KeyboardButton(text="G55"),
            KeyboardButton(text="G56"),
        ],
        [
            KeyboardButton(text="G57"),
            KeyboardButton(text="G58"),
            KeyboardButton(text="G59"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
)