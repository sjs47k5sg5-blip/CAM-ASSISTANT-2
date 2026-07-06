from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def finish_tool_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Тем же инструментом")],
            [KeyboardButton(text="Другим инструментом")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )