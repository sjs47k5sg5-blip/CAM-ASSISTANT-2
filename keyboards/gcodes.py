from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

gcodes_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="G00"),
            KeyboardButton(text="G01"),
            KeyboardButton(text="G02"),
            KeyboardButton(text="G03"),
        ],
        [
            KeyboardButton(text="G17"),
            KeyboardButton(text="G18"),
            KeyboardButton(text="G19"),
        ],
        [
            KeyboardButton(text="G40"),
            KeyboardButton(text="G41"),
            KeyboardButton(text="G42"),
        ],
        [
            KeyboardButton(text="G43"),
            KeyboardButton(text="G54"),
            KeyboardButton(text="G81"),
        ],
        [
            KeyboardButton(text="G83"),
            KeyboardButton(text="G84"),
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
)