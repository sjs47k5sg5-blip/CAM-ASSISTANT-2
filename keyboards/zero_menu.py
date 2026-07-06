from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def zero_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Центр")],
            [
                KeyboardButton(text="Левый верхний"),
                KeyboardButton(text="Правый верхний")
            ],
            [
                KeyboardButton(text="Левый нижний"),
                KeyboardButton(text="Правый нижний")
            ],
            [
                KeyboardButton(text="⬅️ Назад")
            ]
        ],
        resize_keyboard=True
    )