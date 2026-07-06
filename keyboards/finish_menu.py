from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def finish_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="▶️ Сгенерировать G-код")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )