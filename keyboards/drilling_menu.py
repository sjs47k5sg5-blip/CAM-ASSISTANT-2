from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

drilling_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🕳 Сквозное отверстие"),
            KeyboardButton(text="🕳 Глухое отверстие"),
        ],
        [
            KeyboardButton(text="🌀 Резьба"),
            KeyboardButton(text="🔩 Зенковка"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
            KeyboardButton(text="🏠 Главное меню"),
        ],
    ],
    resize_keyboard=True,
)