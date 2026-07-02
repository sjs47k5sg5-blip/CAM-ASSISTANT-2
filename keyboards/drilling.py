from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

drill_type_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="HSS")],
        [KeyboardButton(text="Твердосплавное")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)