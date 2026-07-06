from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def params_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📏 Размер детали")],
            [KeyboardButton(text="🧱 Материал")],
            [KeyboardButton(text="📍 Ноль детали")],
            [KeyboardButton(text="📍 Ноль Z")],
            [KeyboardButton(text="⚙ Обработка углов")],
            [KeyboardButton(text="📉 Припуск")],
            [KeyboardButton(text="🔧 Инструмент")],
            [KeyboardButton(text="✅ Готово")]
        ],
        resize_keyboard=True
    )