from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📁 Проекты")],
            [KeyboardButton(text="⚙ Фрезерная обработка")],
            [KeyboardButton(text="🕳 Обработка отверстий")],
            [KeyboardButton(text="📚 Пособие")],
            [KeyboardButton(text="ℹ О программе")]
        ],
        resize_keyboard=True
    )