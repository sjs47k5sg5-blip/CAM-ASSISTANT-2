from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def finish_pass_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Да")],
            [KeyboardButton(text="Нет")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )