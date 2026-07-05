from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📁 Проект")
            ],
            [
                KeyboardButton(text="⚙ Фрезерные операции")
            ],
            [
                KeyboardButton(text="🕳 Обработка отверстий")
            ],
            [
                KeyboardButton(text="📚 Справочник")
            ],
            [
                KeyboardButton(text="ℹ О программе")
            ]
        ],
        resize_keyboard=True
    )