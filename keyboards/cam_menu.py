from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# =========================
# MILLING MENU (ГЛАВНОЕ)
# =========================
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


# =========================
# PARAMETERS MENU
# =========================
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