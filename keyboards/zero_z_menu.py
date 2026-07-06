from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def zero_z_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Верх детали")],
            [KeyboardButton(text="Низ детали")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )