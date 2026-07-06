from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def milling_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📐 Контур"),
                KeyboardButton(text="📦 Карман"),
                KeyboardButton(text="📏 Обводка")
            ]
        ],
        resize_keyboard=True
    )


def params_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📏 Размер детали")],
            [KeyboardButton(text="🔧 Инструмент")],
            [KeyboardButton(text="📍 Ноль детали")],
            [KeyboardButton(text="📍 Ноль Z")],
            [KeyboardButton(text="⚙ Углы")],
            [KeyboardButton(text="📉 Припуск")],
            [KeyboardButton(text="🧱 Материал")],
            [KeyboardButton(text="✅ Готово")]
        ],
        resize_keyboard=True
    )