from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def corner_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Радиус")],
            [KeyboardButton(text="Фаска")],
            [KeyboardButton(text="Острые углы")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )