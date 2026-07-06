from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def allowance_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="0"),
                KeyboardButton(text="0.2"),
                KeyboardButton(text="0.5")
            ],
            [
                KeyboardButton(text="⬅️ Назад")
            ]
        ],
        resize_keyboard=True
    )