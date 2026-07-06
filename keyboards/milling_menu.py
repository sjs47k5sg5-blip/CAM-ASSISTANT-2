from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def milling_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📐 Контур")],
            [KeyboardButton(text="📦 Карман")],
            [KeyboardButton(text="📏 Обводка")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )