from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reference_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔩 Резьбы"),
            KeyboardButton(text="📏 Допуски"),
        ],
        [
            KeyboardButton(text="🧱 Материалы"),
            KeyboardButton(text="⚙️ G-коды"),
        ],
        [
            KeyboardButton(text="🔧 M-коды"),
            KeyboardButton(text="📊 Скорости резания"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
)