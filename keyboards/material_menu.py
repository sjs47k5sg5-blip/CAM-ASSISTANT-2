from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def material_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Алюминий"),
                KeyboardButton(text="Сталь")
            ],
            [
                KeyboardButton(text="Латунь"),
                KeyboardButton(text="Медь")
            ],
            [
                KeyboardButton(text="⬅️ Назад")
            ]
        ],
        resize_keyboard=True
    )