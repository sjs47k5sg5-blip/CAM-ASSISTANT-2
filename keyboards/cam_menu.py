from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def milling_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📐 Контур"),
                KeyboardButton(text="📦 Карман"),
                KeyboardButton(text="📏 Обводка")
            ],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )


def params_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📏 Размеры детали")],
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


def corner_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Все")],
            [KeyboardButton(text="ЛВ"), KeyboardButton(text="ЛН")],
            [KeyboardButton(text="ПВ"), KeyboardButton(text="ПН")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )


def finish_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ГЕНЕРАЦИЯ")]
        ],
        resize_keyboard=True
    )