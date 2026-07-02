from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reference_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📚 G-коды"),
            KeyboardButton(text="📖 M-коды"),
        ],
        [
            KeyboardButton(text="📐 Материалы"),
            KeyboardButton(text="🛠 Инструменты"),
        ],
        [
            KeyboardButton(text="📏 Допуски"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
)